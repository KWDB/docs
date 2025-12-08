#!/usr/bin/env python3
"""
Markdown 内部链接检查器
检查指定文件夹下所有 Markdown 文档中的内部链接是否有效

使用方法:
1. 将此脚本放在 docs_kaiwuDB/static 目录下
2. 直接运行: python check_md_links.py
   (将自动检查 docs_kaiwuDB 目录下的所有 Markdown 文件)
3. 或指定目录: python check_md_links.py /path/to/docs

注意:默认会排除 static、node_modules、.git 等目录
"""

import os
import re
import sys
from pathlib import Path
from urllib.parse import unquote
from collections import defaultdict


class MarkdownLinkChecker:
    def __init__(self, root_dir, verbose=False, debug=False):
        self.root_dir = Path(root_dir).resolve()
        self.all_files = set()
        self.broken_links = defaultdict(list)
        self.total_links = 0
        self.broken_count = 0
        self.exclude_dirs = {'static', 'node_modules', '.git', '__pycache__'}  # 排除的目录
        self.file_anchors_cache = {}  # 缓存每个文件的锚点列表
        self.verbose = verbose  # 详细模式
        self.debug = debug  # 调试模式
        self.skipped_placeholders = defaultdict(list)  # 记录被跳过的占位符
        
    def find_all_markdown_files(self):
        """查找所有 Markdown 文件"""
        for file_path in self.root_dir.rglob("*.md"):
            if file_path.is_file():
                # 检查文件路径中是否包含需要排除的目录
                if not any(excluded in file_path.parts for excluded in self.exclude_dirs):
                    self.all_files.add(file_path.resolve())
        
        print(f"📁 找到 {len(self.all_files)} 个 Markdown 文件")
        return self.all_files
    
    def extract_anchors_from_file(self, file_path):
        """从 Markdown 文件中提取所有可用的锚点"""
        if file_path in self.file_anchors_cache:
            return self.file_anchors_cache[file_path]
        
        anchors = set()
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            print(f"⚠️  无法读取文件 {file_path} 的锚点: {e}")
            return anchors
        
        # 1. 提取标题锚点 (# 标题)
        # Markdown 标题会自动生成锚点，重复标题会添加 -1, -2, -3 等后缀
        # 改进：更宽松的标题匹配模式，支持标题中的各种格式
        header_pattern = r'^(#{1,6})\s+(.+)$'
        anchor_counts = {}  # 记录每个锚点出现的次数
        
        for match in re.finditer(header_pattern, content, re.MULTILINE):
            level = match.group(1)
            header_text = match.group(2).strip()
            
            # 移除标题中的链接语法
            header_text = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', header_text)
            # 移除 Markdown 语法（反引号、粗体、斜体等）
            # 注意：不移除下划线 _ ，因为它可能是标识符的一部分
            header_text = re.sub(r'[`*~]', '', header_text)
            # 移除 HTML 标签
            header_text = re.sub(r'<[^>]+>', '', header_text)
            # 移除前后空格
            header_text = header_text.strip()
            
            if not header_text:
                continue
            
            # 生成多种可能的锚点格式
            anchor_variants = self.generate_anchor_variants(header_text)
            
            # 对每种锚点变体都处理重复编号
            for anchor in anchor_variants:
                # 处理重复锚点
                if anchor in anchor_counts:
                    # 这是重复的标题，添加带编号的版本
                    anchor_counts[anchor] += 1
                    numbered_anchor = f"{anchor}-{anchor_counts[anchor]}"
                    anchors.add(numbered_anchor)
                else:
                    # 第一次出现的标题
                    anchor_counts[anchor] = 0
                    anchors.add(anchor)
        
        # 2. 提取 HTML 锚点 (<a name="xxx"> 或 <a id="xxx">)
        html_anchor_pattern = r'<a\s+(?:name|id)=["\']([^"\']+)["\']'
        for match in re.finditer(html_anchor_pattern, content, re.IGNORECASE):
            anchors.add(match.group(1))
        
        # 3. 提取 HTML id 属性 (<div id="xxx">)
        html_id_pattern = r'<[^>]+\s+id=["\']([^"\']+)["\']'
        for match in re.finditer(html_id_pattern, content, re.IGNORECASE):
            anchors.add(match.group(1))
        
        self.file_anchors_cache[file_path] = anchors
        return anchors
    
    def generate_anchor_variants(self, header_text):
        """
        生成锚点 ID 的两种变体
        1. 移除点号和下划线（渲染器实际生成的）
        2. 移除点号，保留下划线（手写链接常用的格式）
        """
        variants = set()
        
        # 变体1: 移除点号和下划线（渲染器实际行为）
        anchor1 = header_text.lower()
        anchor1 = re.sub(r'[^\w\s\u4e00-\u9fff-]', '', anchor1)  # 移除点号等，\w包含下划线
        anchor1 = anchor1.replace('_', '')  # 移除下划线
        anchor1 = re.sub(r'\s+', '-', anchor1)
        anchor1 = re.sub(r'-+', '-', anchor1)
        anchor1 = anchor1.strip('-')
        if anchor1:
            variants.add(anchor1)
        
        # 变体2: 移除点号，保留下划线（手写链接格式）
        anchor2 = header_text.lower()
        anchor2 = re.sub(r'[^\w\s\u4e00-\u9fff-]', '', anchor2)  # \w包含下划线，所以下划线被保留
        anchor2 = re.sub(r'\s+', '-', anchor2)
        anchor2 = re.sub(r'-+', '-', anchor2)
        anchor2 = anchor2.strip('-')
        if anchor2:
            variants.add(anchor2)
        
        return variants
    
    
    def extract_links(self, content):
        """提取 Markdown 中的所有链接"""
        links = []
        
        # 1. 匹配 [text](link) 格式的链接
        # 改进：不允许 text 和 link 部分包含换行符，避免跨行匹配表格内容
        markdown_links = re.findall(r'\[([^\]\n]+)\]\(([^\)\n]+)\)', content)
        links.extend(markdown_links)
        
        # 2. 匹配 <link> 格式的链接(但排除 HTML 标签)
        # 只匹配看起来像 URL 的内容,不匹配 HTML 标签
        angle_bracket_pattern = r'<((?!/)(?![a-zA-Z]+\s)[^>\s]+)>'
        angle_links = re.findall(angle_bracket_pattern, content)
        # 过滤掉 http/https 开头的外部链接
        angle_links = [(link, link) for link in angle_links 
                       if not link.startswith(('http://', 'https://', 'mailto:', 'tel:'))]
        links.extend(angle_links)
        
        return links
    
    def is_internal_link(self, link):
        """判断是否为内部链接"""
        # 排除外部链接
        if link.startswith(('http://', 'https://', 'ftp://', 'mailto:', 'tel:')):
            return False
        
        # 排除邮箱地址
        if '@' in link:
            # 简单的邮箱格式检查
            if re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', link):
                return False
        
        # 排除域名 (www.xxx.com 或 xxx.com 格式,但不以 http 开头)
        if '.' in link and not link.startswith(('./', '../')):
            # 检查是否为域名格式(但不是文件路径)
            if re.match(r'^(www\.)?[a-z0-9-]+(\.[a-z0-9-]+)*\.[a-z]{2,}$', link, re.IGNORECASE):
                return False
        
        # 检查是否为占位符 - 这个检查应该对所有非路径链接生效
        if self._is_likely_placeholder(link):
            return False
        
        return True
    
    def _is_likely_placeholder(self, link):
        """判断是否为占位符或代码引用"""
        # 首先排除明显的文件路径
        # 以 ./ 或 ../ 或 / 开头的是文件路径
        if link.startswith(('./', '../', '/')):
            return False
        
        # 包含常见文件扩展名的可能是真实文件(但排除 .h 头文件)
        common_extensions = ['.md', '.html', '.htm', '.pdf', '.doc', '.docx', 
                           '.txt', '.json', '.xml', '.yaml', '.yml', '.png', 
                           '.jpg', '.jpeg', '.gif', '.svg']
        for ext in common_extensions:
            if link.endswith(ext):
                return False
        
        # 常见的占位符模式
        placeholder_patterns = [
            # SQL/数据库相关
            r'^[a-z_]+_name$',           # xxx_name 格式
            r'^[a-z_]+_list$',           # xxx_list 格式
            r'^[a-z_]+_elem$',           # xxx_elem 格式
            r'^[a-z_]+_expr$',           # xxx_expr 格式
            r'^[a-z]+_[a-z]+_[a-z]+$',   # xxx_xxx_xxx 格式
            r'^[a-z]+_[a-z]+$',          # xxx_xxx 格式(两段式)
            
            # 编程语言相关(Java, C#, Python等)
            r'^[A-Z][a-zA-Z0-9]*(?:Entity|Data|Type|Class|Info|Group|Log|Version|Framework|Namespace|Using|Usings)$',  # Java实体类等
            r'^[a-z]+\.[a-z]+(?:\.[a-z]+)*$',  # 属性格式 (如 project.build.sourceEncoding)
            r'^[a-z_]+\.[a-z_]+$',       # 带下划线的属性格式 (如 meta.sql_path)
            r'^[a-z]+Id$',               # xxxId 格式 (如 groupId, artifactId)
            r'^[A-Z][a-z]{1,5}$',        # 短类名 (如 Row, Utc, String) - 首字母大写,后面1-5个小写字母
            r'^u[0-9]+$',                # Rust类型 (如 u8, u16, u32, u64)
            r'^[A-Z][a-z]+[A-Z][a-z]+',  # 驼峰命名 (如 TargetFramework, RootNamespace)  
            
            # 通用占位符
            r'^name$|^value$|^id$|^key$|^option$|^param$|^arg$',
            
            # HTML/XML 标签
            r'^br/?$|^hr$|^div$|^span$',
            
            # 特殊格式
            r'^[a-z]+\{[^}]+\}$',        # 花括号格式
            r'^[a-z]+\([^)]*\)$',        # 圆括号格式
            r'^[a-z_]+:[a-z_0-9]+$',     # 冒号格式 (如 krb5_host_address:ip, ip:port)
            r'^[a-z]+-[a-z]+-[a-z]+$',   # 连字符格式 (如 key-path, storage-path)
            r'^[a-z]+-[a-z]+$',          # 两段连字符 (如 your-host-ip)
            
            # C/C++ 头文件
            r'^[a-z_]+\.h$',             # xxx.h 格式 (如 windows.h, stdio.h)
            
            # 代码/配置相关
            r'^base64\([^)]+\)$',        # base64(xxx) 格式
            
            # 单引号包裹的占位符
            r"^'[^']+'\s*$",             # 'xxx' 格式
            
            # 数字结尾的变量
            r'^[a-z_]+[0-9]+$',          # xxx1, xxx2 格式 (如 text1, int1, tag1)
            
            # 路径占位符(斜杠结尾或包含斜杠)
            r'^[a-zA-Z_]+/$',            # xxx/ 格式 (如 relativePath/)
            r'^[a-z]+/[a-z]+$',          # xxx/yyy 格式 (如 addr/host)
            
            # HTML 注释格式
            r'^!--[^-]+-*$',             # HTML 注释 (如 !--Request--, !--请求--)
            
            # 中文占位符
            r'^[\u4e00-\u9fff]+$',       # 纯中文 (如 聚合函数, 版本号, 无)
            
            # 中文符号相关(来自错误链接)
            r'^[`（）、=<>]+$',           # 纯符号
        ]
        
        for pattern in placeholder_patterns:
            if re.match(pattern, link, re.IGNORECASE):
                return True
        
        # 如果链接全是小写字母、数字和下划线,且长度较短(<30字符),也认为是占位符
        if re.match(r'^[a-z0-9_]+$', link) and len(link) < 30:
            # 但排除可能的真实文件名(如 README, index 等)
            common_filenames = {'readme', 'index', 'home', 'main', 'config'}
            if link.lower() not in common_filenames:
                return True
        
        # 如果是全大写字母(SQL 命令等),也认为是占位符
        if re.match(r'^[A-Z]+$', link) and len(link) > 3:
            return True
        
        # 如果包含多个下划线且较长(超过20字符),也认为是占位符
        if '_' in link and len(link) > 20:
            return True
        
        # 特殊情况:连字符格式的配置项
        if '-' in link and not '/' in link:
            # 如 key-path, storage-path, old-key-path 等
            parts = link.split('-')
            if all(len(part) > 0 and part.islower() for part in parts):
                return True
        
        # 特殊情况:冒号分隔的格式(如 ip:port, host:port)
        if ':' in link and not link.startswith(('http:', 'https:', 'ftp:', 'mailto:')):
            parts = link.split(':')
            if len(parts) == 2 and all(len(part) > 0 for part in parts):
                # 都是小写字母/数字/下划线
                if all(re.match(r'^[a-z0-9_]+$', part) for part in parts):
                    return True
        
        # 特殊情况:包含斜杠但看起来像占位符(如 addr/host, br/)
        # 注意:以 / 开头的已在方法开头被排除
        if '/' in link:
            parts = link.split('/')
            if len(parts) == 2:
                # 都是简单的小写字母或空字符串
                if all(re.match(r'^[a-z]*$', part) for part in parts):
                    return True
        
        # 特殊情况:包含中文符号的异常链接(通常是 Markdown 渲染问题)
        if any(char in link for char in ['`', ')', '、', '等号', '(']):
            return True
        
        return False
    
    def check_link(self, source_file, link):
        """检查单个链接是否有效,包括文件和锚点"""
        # 分离文件路径和锚点
        if '#' in link:
            link_parts = link.split('#', 1)
            link_without_anchor = link_parts[0]
            anchor = link_parts[1]
        else:
            link_without_anchor = link
            anchor = None
        
        # 如果是纯锚点链接(#section),检查当前文件
        if not link_without_anchor and anchor:
            target_file = source_file
        elif link_without_anchor:
            # URL 解码
            link_without_anchor = unquote(link_without_anchor)
            
            # 构建目标文件路径
            if link_without_anchor.startswith('/'):
                # 绝对路径(相对于根目录)
                target_file = (self.root_dir / link_without_anchor.lstrip('/')).resolve()
            else:
                # 相对路径(相对于当前文件)
                target_file = (source_file.parent / link_without_anchor).resolve()
            
            # 检查文件是否存在
            if not target_file.exists():
                return False, "文件不存在"
        else:
            # 空链接
            return False, "空链接"
        
        # 如果有锚点,检查锚点是否存在
        if anchor:
            # URL 解码锚点
            anchor = unquote(anchor)
            
            # 只检查 Markdown 文件的锚点
            if target_file.suffix.lower() == '.md':
                available_anchors = self.extract_anchors_from_file(target_file)
                if anchor not in available_anchors:
                    # 调试模式：显示可用的锚点
                    if self.debug:
                        print(f"\n🔍 调试信息:")
                        print(f"   目标文件: {target_file.name}")
                        print(f"   查找锚点: #{anchor}")
                        print(f"   可用锚点中包含关键词的:")
                        keywords = ['kwdb', 'login', 'license', 'user', 'internal']
                        for a in sorted(available_anchors):
                            if any(kw in a.lower() for kw in keywords):
                                print(f"      #{a}")
                    return False, f"锚点不存在: #{anchor}"
        
        return True, None
    
    def check_file(self, file_path):
        """检查单个 Markdown 文件中的所有链接"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            print(f"⚠️  无法读取文件 {file_path}: {e}")
            return
        
        links = self.extract_links(content)
        
        for text, link in links:
            # 使用 is_internal_link 来过滤,它会自动排除外部链接、邮箱、域名和占位符
            if not self.is_internal_link(link):
                if self.verbose:
                    # 记录被跳过的非外部链接(占位符等)
                    if not link.startswith(('http://', 'https://', 'ftp://', 'mailto:', 'tel:')):
                        self.skipped_placeholders[file_path].append({
                            'text': text,
                            'link': link
                        })
                continue
            
            # 这是真实的内部链接
            self.total_links += 1
            
            is_valid, error_msg = self.check_link(file_path, link)
            if not is_valid:
                self.broken_count += 1
                self.broken_links[file_path].append({
                    'text': text,
                    'link': link,
                    'error': error_msg
                })
    
    def check_all(self):
        """检查所有文件"""
        self.find_all_markdown_files()
        
        print(f"\n🔍 开始检查内部链接...\n")
        
        for file_path in self.all_files:
            self.check_file(file_path)
        
        self.print_report()
    
    def print_report(self):
        """打印检查报告并输出到 Markdown 文件"""
        print("\n" + "="*70)
        print("📊 检查报告")
        print("="*70)
        
        # 统计被过滤的占位符
        total_placeholders = sum(len(items) for items in self.skipped_placeholders.values())
        
        print(f"总共检查了 {self.total_links} 个内部链接")
        if total_placeholders > 0:
            print(f"跳过了 {total_placeholders} 个占位符/代码引用")
        print(f"发现 {self.broken_count} 个失效链接")
        
        # 生成 Markdown 报告
        report_lines = []
        report_lines.append("# Markdown 链接检查报告\n")
        report_lines.append(f"**检查时间**: {self._get_current_time()}\n")
        report_lines.append(f"**检查目录**: `{self.root_dir}`\n")
        report_lines.append(f"**Markdown 文件数**: {len(self.all_files)}\n")
        report_lines.append(f"**内部链接总数**: {self.total_links}\n")
        if total_placeholders > 0:
            report_lines.append(f"**跳过的占位符/代码引用**: {total_placeholders}\n")
        report_lines.append(f"**失效链接数**: {self.broken_count}\n")
        report_lines.append("\n---\n\n")
        
        if self.broken_links:
            print("\n❌ 失效链接详情:\n")
            report_lines.append("## ❌ 失效链接详情\n\n")
            
            for file_path, links in sorted(self.broken_links.items()):
                rel_path = file_path.relative_to(self.root_dir)
                print(f"📄 {rel_path}")
                report_lines.append(f"### 📄 `{rel_path}`\n\n")
                
                for link_info in links:
                    print(f"   ├─ [{link_info['text']}]({link_info['link']})")
                    print(f"   │  错误: {link_info['error']}")
                    
                    # Markdown 格式 - 直接显示原文
                    report_lines.append(f"- `[{link_info['text']}]({link_info['link']})`\n")
                    report_lines.append(f"  - 错误: {link_info['error']}\n\n")
                
                print()
                report_lines.append("\n")
        else:
            print("\n✅ 所有内部链接都有效!")
            report_lines.append("## ✅ 检查结果\n\n")
            report_lines.append("所有内部链接都有效！\n\n")
        
        # 详细模式:显示被跳过的占位符
        if self.verbose and self.skipped_placeholders:
            print("\n" + "="*70)
            print("ℹ️  被跳过的占位符/代码引用 (详细模式)")
            print("="*70)
            
            report_lines.append("---\n\n")
            report_lines.append("## ℹ️ 被跳过的占位符/代码引用\n\n")
            report_lines.append("*以下内容仅在详细模式 (--verbose) 下显示*\n\n")
            
            for file_path, placeholders in sorted(self.skipped_placeholders.items()):
                rel_path = file_path.relative_to(self.root_dir)
                print(f"\n📄 {rel_path} ({len(placeholders)} 个)")
                report_lines.append(f"### 📄 `{rel_path}` ({len(placeholders)} 个)\n\n")
                
                unique_placeholders = {}
                for p in placeholders:
                    link = p['link']
                    if link not in unique_placeholders:
                        unique_placeholders[link] = 0
                    unique_placeholders[link] += 1
                
                for link, count in sorted(unique_placeholders.items()):
                    if count > 1:
                        print(f"   ├─ [{link}]({link}) (x{count})")
                        report_lines.append(f"- `{link}` (出现 {count} 次)\n")
                    else:
                        print(f"   ├─ [{link}]({link})")
                        report_lines.append(f"- `{link}`\n")
                
                report_lines.append("\n")
            print()
        
        print("="*70)
        
        # 将报告写入 Markdown 文件 - 保存到 docs_kaiwuDB 的父目录
        report_path = self.root_dir.parent / "link_check_report.md"
        try:
            with open(report_path, 'w', encoding='utf-8') as f:
                f.writelines(report_lines)
            print(f"\n📝 报告已保存到: {report_path}")
        except Exception as e:
            print(f"\n⚠️  无法保存报告文件: {e}")
    
    def _get_current_time(self):
        """获取当前时间字符串"""
        from datetime import datetime
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def main():
    # 检查是否有 --verbose 或 -v 参数
    verbose = '--verbose' in sys.argv or '-v' in sys.argv
    debug = '--debug' in sys.argv or '-d' in sys.argv
    
    if verbose:
        sys.argv = [arg for arg in sys.argv if arg not in ['--verbose', '-v']]
    if debug:
        sys.argv = [arg for arg in sys.argv if arg not in ['--debug', '-d']]
    
    # 如果没有提供参数,默认检查脚本所在目录的上一级目录(docs_kaiwuDB)
    if len(sys.argv) < 2:
        script_dir = Path(__file__).parent
        target_dir = script_dir.parent  # 上一级目录
        print(f"💡 未指定目录,使用默认目录: {target_dir}")
    else:
        target_dir = sys.argv[1]
    
    target_dir = Path(target_dir)
    
    if not target_dir.is_dir():
        print(f"❌ 错误: '{target_dir}' 不是一个有效的文件夹")
        print("\n用法: python check_md_links.py [文件夹路径] [--verbose] [--debug]")
        print("示例: python check_md_links.py ../")
        print("示例: python check_md_links.py --verbose  # 显示被跳过的占位符")
        print("示例: python check_md_links.py --debug  # 显示锚点调试信息")
        print("如果不提供路径,将检查脚本所在目录的上一级目录")
        sys.exit(1)
    
    if verbose:
        print("🔍 详细模式:将显示被跳过的占位符信息")
    if debug:
        print("🐛 调试模式:将显示锚点匹配详情")
    
    checker = MarkdownLinkChecker(target_dir, verbose=verbose, debug=debug)
    checker.check_all()


if __name__ == "__main__":
    main()