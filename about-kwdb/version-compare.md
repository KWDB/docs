---
title: 版本功能对比
id: version-compare
---

# 版本功能对比

KaiwuDB 提供企业版（KaiwuDB）与开源版（KWDB）两种版本。企业版面向对数据安全、高可用和运维管理有严格要求的生产环境，提供全功能支持与专业售后服务；开源版保留核心功能模块，由社区驱动，适合开发者快速上手与技术探索。如需了解更多功能详情或申请试用企业版，欢迎[联系我们](https://www.kaiwudb.com/about/support)。

<table>
  <thead>
    <tr>
      <th colspan="3" style="text-align:left">功能描述</th>
      <th>企业版（KaiwuDB）</th>
      <th>开源版（KWDB）</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td rowspan="8">多模引擎</td>
      <td rowspan="6">时序引擎</td>
      <td><a href="../db-administration/data-stream.md">流计算</a></td><td>✅</td><td>✅</td>
    </tr>
    <tr><td>数据发布</td><td>✅</td><td>—</td></tr>
    <tr><td>数据订阅</td><td>✅</td><td>—</td></tr>
    <tr><td><a href="../db-operation/storage-mgmt.md">数据压缩</a></td><td>✅</td><td>✅</td></tr>
    <tr><td>冷热分级存储</td><td>✅</td><td>—</td></tr>
    <tr><td><a href="./product-features.md#生命周期管理">生命周期管理</a></td><td>✅</td><td>✅</td></tr>
    <tr><td colspan="2">关系引擎</td><td>✅</td><td>✅</td></tr>
    <tr><td colspan="2">AI 预测分析引擎</td><td>✅</td><td>—</td></tr>
    <tr>
      <td rowspan="6">灵活部署</td>
      <td colspan="2"><a href="../quickstart/overview.md">单机部署</a></td><td>✅</td><td>✅</td>
    </tr>
    <tr><td colspan="2"><a href="../quickstart/overview.md">容器部署</a></td><td>✅</td><td>✅</td></tr>
    <tr><td rowspan="2"><a href="../deployment/overview.md">集群部署</a></td><td>单副本</td><td>✅</td><td>✅</td></tr>
    <tr><td>三副本及以上</td><td>✅</td><td>✅</td></tr>
    <tr><td rowspan="2">主备部署</td><td>单机主备</td><td>✅</td><td>—</td></tr>
    <tr><td>集群主备</td><td>✅</td><td>—</td></tr>
    <tr>
      <td rowspan="6">运维管理</td>
      <td colspan="2"><a href="../kaiwudb-tools/kat/kat-overview.md">KAT 智能化运维工具</a></td><td>✅</td><td>—</td>
    </tr>
    <tr><td colspan="2">备份还原</td><td>✅</td><td>—</td></tr>
    <tr>
      <td colspan="2"><a href="../db-monitor/deploy-monitoring.md">监控工具</a></td>
      <td>✅<br><small style="color:gray">开箱即用，无需额外配置</small></td>
      <td>✅</td>
    </tr>
    <tr><td colspan="2"><a href="../kaiwudb-tools/kaiwudb-developer-center/overview.md">客户端工具</a></td><td>✅</td><td>✅</td></tr>
    <tr>
      <td colspan="2"><a href="../db-migration/migration.md">迁移工具</a></td>
      <td>✅<br><small style="color:gray">支持元数据及数据可视化同步</small></td>
      <td>✅<br><small style="color:gray">支持数据同步</small></td>
    </tr>
    <tr>
      <td colspan="2"><a href="../kaiwudb-tools/perf-benchmark/kwdb-tsbs.md">性能测试工具</a></td>
      <td>✅<br><small style="color:gray">KaiwuDB Benchmark</small></td>
      <td>✅<br><small style="color:gray">TSBS</small></td>
    </tr>
    <tr>
      <td rowspan="9">安全策略</td>
      <td colspan="2"><a href="../db-security/privilege-mgmt.md">用户权限管理</a></td>
      <td>✅<br><small style="color:gray">支持列级权限</small></td>
      <td>✅</td>
    </tr>
    <tr><td colspan="2"><a href="../db-security/identity-authn.md">身份认证</a></td><td>✅</td><td>✅</td></tr>
    <tr><td colspan="2"><a href="../db-security/identity-authn.md#基于主机的认证">白名单</a></td><td>✅</td><td>✅</td></tr>
    <tr><td colspan="2"><a href="../db-security/audit-mgmt.md">审计日志</a></td><td>✅</td><td>✅</td></tr>
    <tr>
      <td colspan="2"><a href="../db-security/transport-encryption.md">加密传输</a></td>
      <td>✅<br><small style="color:gray">支持国密算法</small></td>
      <td>✅</td>
    </tr>
    <tr><td colspan="2">三权分立</td><td>✅</td><td>—</td></tr>
    <tr><td colspan="2">强制访问控制</td><td>✅</td><td>—</td></tr>
    <tr><td colspan="2">SQL 防注入</td><td>✅</td><td>—</td></tr>
    <tr><td colspan="2">加密存储</td><td>✅</td><td>—</td></tr>
    <tr>
      <td rowspan="6">生态兼容</td>
      <td colspan="2"><a href="../third-party-tools/kafka.md">Kafka</a></td><td>✅</td><td>✅</td>
    </tr>
    <tr><td colspan="2"><a href="../third-party-tools/flink.md">Flink</a></td><td>✅</td><td>✅</td></tr>
    <tr><td colspan="2"><a href="../third-party-tools/emqx.md">EMQX</a></td><td>✅</td><td>✅</td></tr>
    <tr><td colspan="2"><a href="../third-party-tools/datax.md">DataX</a></td><td>✅</td><td>✅</td></tr>
    <tr><td colspan="2">国产化兼容</td><td>✅</td><td>—</td></tr>
    <tr><td colspan="2"><a href="../development/overview.md">主流编程语言</a></td><td>✅</td><td>✅</td></tr>
    <tr>
      <td rowspan="3">增值服务</td>
      <td colspan="2">最佳实践</td><td>✅</td><td>—</td>
    </tr>
    <tr><td colspan="2">使用培训</td><td>✅</td><td>—</td></tr>
    <tr>
      <td colspan="2">技术支持</td>
      <td>✅<br><small style="color:gray">7×24h 专业售后支持</small></td>
      <td>✅<br><small style="color:gray">社区支持</small></td>
    </tr>
  </tbody>
</table>