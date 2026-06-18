---
title: Version Comparison
id: version-compare
---

# Version Comparison

KaiwuDB is available in two editions: the Enterprise Edition (KaiwuDB) and the Open-Source Edition (KWDB). The Enterprise Edition is designed for production environments with strict requirements around data security, high availability, and operational management, offering full-featured support and professional after-sales service. The Open-Source Edition retains core functional modules and is community-driven, making it ideal for developers who want to get started quickly or explore the technology. To learn more about specific features or request a trial of the Enterprise Edition, please [contact us](https://www.kaiwudb.com/about/support).

<table>
  <thead>
    <tr>
      <th colspan="3" style="text-align:left">Feature</th>
      <th>Enterprise Edition (KaiwuDB)</th>
      <th>Open-Source Edition (KWDB)</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td rowspan="8">Multi-Model Engine</td>
      <td rowspan="6">Time-Series Engine</td>
      <td><a href="../db-administration/data-stream.md">Stream Computing</a></td><td>✅</td><td>✅</td>
    </tr>
    <tr><td>Data Publication</td><td>✅</td><td>—</td></tr>
    <tr><td>Data Subscription</td><td>✅</td><td>—</td></tr>
    <tr><td><a href="../db-operation/storage-mgmt.md">Data Compression</a></td><td>✅</td><td>✅</td></tr>
    <tr><td>Tiered Hot/Cold Storage</td><td>✅</td><td>—</td></tr>
    <tr><td><a href="./product-features.md#lifecycle-management">Lifecycle Management</a></td><td>✅</td><td>✅</td></tr>
    <tr><td colspan="2">Relational Engine</td><td>✅</td><td>✅</td></tr>
    <tr><td colspan="2">AI Predictive Analytics Engine</td><td>✅</td><td>—</td></tr>
    <tr>
      <td rowspan="7">Flexible Deployment</td>
      <td colspan="2"><a href="../quickstart/overview.md">Standalone Deployment</a></td><td>✅</td><td>✅</td>
    </tr>
    <tr><td colspan="2"><a href="../quickstart/overview.md">Container Deployment</a></td><td>✅</td><td>✅</td></tr>
    <tr><td rowspan="3"><a href="../deployment/overview.md">Cluster Deployment</a></td><td>Single Replica</td><td>✅</td><td>✅</td></tr></a></td><td>Dual Replica</td><td>✅</td><td>—</td></tr>
    <tr><td>Three or More Replicas</td><td>✅</td><td>✅</td></tr>
    <tr><td rowspan="2">Primary-Standby Deployment</td><td>Standalone Primary-Standby</td><td>✅</td><td>—</td></tr>
    <tr><td>Cluster Primary-Standby</td><td>✅</td><td>—</td></tr>
    <tr>
      <td rowspan="6">Operations & Management</td>
      <td colspan="2"><a href="../kaiwudb-tools/kat/kat-overview.md">KAT Intelligent O&M Tool</a></td><td>✅</td><td>—</td>
    </tr>
    <tr><td colspan="2">Backup & Restore</td><td>✅</td><td>—</td></tr>
    <tr>
      <td colspan="2"><a href="../db-monitor/deploy-monitoring.md">Monitoring Tools</a></td>
      <td>✅<br><small style="color:gray">Ready to use out of the box, no additional configuration required</small></td>
      <td>✅</td>
    </tr>
    <tr><td colspan="2"><a href="../kaiwudb-tools/kaiwudb-developer-center/overview.md">Client Tools</a></td><td>✅</td><td>✅</td></tr>
    <tr>
      <td colspan="2"><a href="../db-migration/migration.md">Migration Tools</a></td>
      <td>✅<br><small style="color:gray">Supports metadata and data visual synchronization</small></td>
      <td>✅<br><small style="color:gray">Supports data synchronization</small></td>
    </tr>
    <tr>
      <td colspan="2"><a href="../kaiwudb-tools/perf-benchmark/kwdb-tsbs.md">Performance Benchmarking Tools</a></td>
      <td>✅<br><small style="color:gray">KaiwuDB Benchmark</small></td>
      <td>✅<br><small style="color:gray">TSBS</small></td>
    </tr>
    <tr>
      <td rowspan="9">Security Policies</td>
      <td colspan="2"><a href="../db-security/privilege-mgmt.md">User Privilege Management</a></td>
      <td>✅<br><small style="color:gray">Supports column-level privileges</small></td>
      <td>✅</td>
    </tr>
    <tr><td colspan="2"><a href="../db-security/identity-authn.md">Identity Authentication</a></td><td>✅</td><td>✅</td></tr>
    <tr><td colspan="2"><a href="../db-security/identity-authn.md#host-based-authentication">Allowlist</a></td><td>✅</td><td>✅</td></tr>
    <tr><td colspan="2"><a href="../db-security/audit-mgmt.md">Audit Logging</a></td><td>✅</td><td>✅</td></tr>
    <tr>
      <td colspan="2"><a href="../db-security/transport-encryption.md">Encrypted Transmission</a></td>
      <td>✅<br><small style="color:gray">Supports Chinese cryptographic algorithms</small></td>
      <td>✅</td>
    </tr>
    <tr><td colspan="2">Separation of Duties</td><td>✅</td><td>—</td></tr>
    <tr><td colspan="2">Mandatory Access Control</td><td>✅</td><td>—</td></tr>
    <tr><td colspan="2">SQL Injection Prevention</td><td>✅</td><td>—</td></tr>
    <tr><td colspan="2">Encrypted Storage</td><td>✅</td><td>—</td></tr>
    <tr>
      <td rowspan="6">Ecosystem Compatibility</td>
      <td colspan="2"><a href="../third-party-tools/kafka.md">Kafka</a></td><td>✅</td><td>✅</td>
    </tr>
    <tr><td colspan="2"><a href="../third-party-tools/flink.md">Flink</a></td><td>✅</td><td>✅</td></tr>
    <tr><td colspan="2"><a href="../third-party-tools/emqx.md">EMQX</a></td><td>✅</td><td>✅</td></tr>
    <tr><td colspan="2"><a href="../third-party-tools/datax.md">DataX</a></td><td>✅</td><td>✅</td></tr>
    <tr><td colspan="2">Domestic Hardware & OS Compatibility</td><td>✅</td><td>—</td></tr>
    <tr><td colspan="2"><a href="../development/overview.md">Mainstream Programming Languages</a></td><td>✅</td><td>✅</td></tr>
    <tr>
      <td rowspan="3">Value-Added Services</td>
      <td colspan="2">Best Practices</td><td>✅</td><td>—</td>
    </tr>
    <tr><td colspan="2">Training</td><td>✅</td><td>—</td></tr>
    <tr>
      <td colspan="2">Technical Support</td>
      <td>✅<br><small style="color:gray">24/7 professional after-sales support</small></td>
      <td>✅<br><small style="color:gray">Community support</small></td>
    </tr>
  </tbody>
</table>