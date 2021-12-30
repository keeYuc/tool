# tool
#### color 给日志加颜色 方便日志查看
tail -f ... |color
#### port-tool 一键k8s 命令
```bash
测试环境正式环境pod相关 快捷命令

pfw  >>> 一键端口映射 默认参数 -c seo -n gcp -p 9009

pexec >>> 一键进入pod 默认参数 -c crawler -n gcp -s sh <有多个健康pod时可以自主选择>

plog  >>> 一键查看pod日志 默认参数为 -c seo -n gcp -t 100 <有多个健康pod时可以自主选择>

```
#### kube-log 是方便在K8s上直接看日志 
#### code-builder go中间件多态生成器
