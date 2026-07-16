window.GUIDE_SITE_DATA = {
  "asset_fingerprints": {
    "assets/site.css": "fffc015e09ec2df287e11189b92aa951db920a59208355e2755fd3412550c080",
    "assets/site.js": "59423ac374ef053874fb1615d4c99b5ab28006cf53cccf21d51a98c2cbc0688e",
    "assets/theme.js": "187420686654f8c1c58df32a0687d4a0d11e6e0707b8696d5f077774982d766a",
    "figures/social-preview.png": "e0ee23ae3b99a8507b4aa423c530289468f1db067d1e7041e4afcefb5fe3ac58"
  },
  "build_id": "164efa044e15",
  "changelog": [
    {
      "category": "quality",
      "date": "2026-07-16",
      "summary": "Mermaid 流程图尺寸；权限、MCP、Subagents、提示词四页的小黑配图；配图图注与替代文本。",
      "target": "install-desktop.html#安装到第一个任务",
      "title": "调整流程图与正文配图"
    },
    {
      "category": "quality",
      "date": "2026-07-16",
      "summary": "逐页资料依据、首页更新日志、权限模式表述、Skill／Plugin／MCP 分层、页脚内容与全页面响应式适配。",
      "target": "index.html#最近更新",
      "title": "补齐资料依据与页面信息"
    },
    {
      "category": "content",
      "date": "2026-07-16",
      "summary": "GPT-5.6 prompting guidance 中文解读、refine-user-prompt skill 介绍；移除原 Goal Entry 专题。",
      "target": "prompt-guidance.html",
      "title": "新增 GPT-5.6 提示词指南"
    },
    {
      "category": "content",
      "date": "2026-07-12",
      "summary": "awesome-chatgpt-prompts-zh 仓库说明、Codex 使用示例与提示词安全边界。",
      "target": "skills-repositories.html",
      "title": "新增中文 Prompt 仓库条目"
    },
    {
      "category": "content",
      "date": "2026-07-12",
      "summary": "taste-skill 与 Ian Xiaohei Illustrations 的仓库说明、使用示例和适用边界。",
      "target": "skills-repositories.html",
      "title": "新增视觉与中文配图 Skills"
    },
    {
      "category": "content",
      "date": "2026-07-12",
      "summary": "Skills、MCP、辅助工具榜单与官方基础设施条目。",
      "target": "skills-repositories.html",
      "title": "新增 Codex 生态 Top 10"
    },
    {
      "category": "structure",
      "date": "2026-07-11",
      "summary": "统一站点清单、首页最近更新、完整更新日志与站点生成数据。",
      "target": "index.html",
      "title": "新增站点清单与更新日志"
    },
    {
      "category": "content",
      "date": "2026-07-10",
      "summary": "第三方 Skills 仓库对比、任务选择表与安装入口。",
      "target": "skills-repositories.html",
      "title": "新增 Skills 仓库选择指南"
    },
    {
      "category": "content",
      "date": "2026-07-07",
      "summary": "插件安装、核心流程与真实实例。",
      "target": "compound-engineering.html",
      "title": "新增 Compound Engineering 指南"
    }
  ],
  "fragments": {
    "agents-md.html": [
      "它是什么",
      "什么时候用-不用",
      "可复制示例",
      "如何设计-agents.md-层级",
      "根目录",
      "子目录",
      "当前任务",
      "写-agents.md-的检查清单",
      "不要把这些写进-agents.md",
      "真实实例-历史复合案例"
    ],
    "automation.html": [
      "什么时候值得自动化",
      "适合-automations",
      "适合后台-worktree",
      "适合本地脚本",
      "自动化前置条件",
      "不该自动化的任务",
      "创建定时任务",
      "逐项配置",
      "配置模板",
      "三种实用自动化模式",
      "只读审查",
      "失败日志解释",
      "文档漂移检查",
      "自动化安全阀",
      "最小权限",
      "结构化输出",
      "人工-checkpoint",
      "失败即停止",
      "无人值守禁区",
      "真实实例-自动检查网页链接和关键标题",
      "输入",
      "先读",
      "应动文件",
      "验证",
      "最终回答",
      "失败停止"
    ],
    "codex.html": [
      "它是什么",
      "什么时候用-不用",
      "可复制示例",
      "真实实例-扩充这份网页手册"
    ],
    "compound-engineering.html": [
      "它是什么",
      "在-codex-desktop-里安装",
      "第一次进入项目后先跑什么",
      "核心七步怎么用",
      "product-contract-和实施计划写在同一份文档",
      "常见情况选哪个-skill",
      "还不知道做什么",
      "这是-bug",
      "在评估外部方案",
      "刚做完一批代码",
      "想全自动交付",
      "可复制输入",
      "使用边界",
      "真实实例-历史案例",
      "请求",
      "先读与角色",
      "边界",
      "验证证据",
      "重要恢复与结果",
      "失败停止"
    ],
    "daily-workflow.html": [
      "日常任务的最小可靠闭环",
      "说明任务",
      "让-codex-读上下文",
      "小范围执行",
      "验证和收口",
      "在桌面版里实际怎么操作",
      "把问题贴进线程",
      "要求先读规则",
      "逐个批准动作",
      "用浏览器反馈迭代",
      "最后看证据",
      "五类高频日常任务",
      "读代码并解释",
      "修失败测试",
      "修改网页或文档",
      "审查当前-diff",
      "提交和发布",
      "坏请求和好请求的差别",
      "不要这样写",
      "推荐这样写",
      "验收不是-看起来完成了",
      "改动证据",
      "验证证据",
      "风险证据",
      "交付证据",
      "推荐-closeout-模板",
      "常见失败和补救",
      "改动太散",
      "没有读上下文",
      "验证跑不通",
      "网页看起来不对",
      "解释太空泛",
      "任务变长了",
      "真实实例-把短页面扩成日常任务手册",
      "输入",
      "先读",
      "应动文件",
      "验证",
      "最终回答",
      "失败停止"
    ],
    "desktop-cli.html": [
      "什么时候优先用-desktop",
      "页面和视觉反馈",
      "本地仓库协作",
      "需要你审批的操作",
      "沉淀为-automations-的场景",
      "不要混用得太乱",
      "desktop-里的六个常用操作",
      "1.-打开任务线程",
      "2.-让-codex-读上下文",
      "3.-用浏览器反馈定位问题",
      "4.-审批有副作用动作",
      "5.-看-diff-和验证结果",
      "6.-发布后抽样确认",
      "desktop-first-prompt-模板",
      "网页反馈",
      "代码修复",
      "需要联网或推送",
      "线程收口",
      "真实实例-本页这次怎么改",
      "输入",
      "执行",
      "验证",
      "交付"
    ],
    "engineering.html": [
      "从-idea-到-task-receipt",
      "双层角色与权限",
      "a2-用户-产品负责人",
      "a3-主线程-编排者",
      "a4-subagent-独立-reviewer",
      "外部写入-grant",
      "自动失效",
      "按依赖和写域组织并行",
      "contract-lane-串行",
      "独立-lanes-并行",
      "更新基线",
      "集成门",
      "可并行示例",
      "失败停止",
      "独立-reviewer-合同",
      "真实实例-历史复合案例",
      "请求",
      "先读",
      "角色",
      "边界-文件",
      "脏主保护",
      "完整-goal",
      "分工",
      "验证证据",
      "独立-review",
      "重要恢复",
      "结果-receipt",
      "失败停止-2",
      "来源分类"
    ],
    "goal.html": [
      "它是什么",
      "什么时候用-不用",
      "可复制示例",
      "一个好-goal-必须包含什么",
      "objective",
      "scope",
      "acceptance",
      "validation",
      "artifacts",
      "stop-conditions",
      "三种常见-goal-模板",
      "真实实例-历史复合案例",
      "验证与重要恢复",
      "结果与回执"
    ],
    "index.html": [
      "最近更新",
      "原生能力与本指南推荐实践",
      "codex-原生能力",
      "本指南推荐实践",
      "选择你的路径",
      "零基础-安装到第一个任务",
      "日常协作-桌面版工作流",
      "进阶用户-任务升级路线",
      "skills-仓库怎么选",
      "工程-学术场景",
      "维护者-资料和发布边界",
      "30-秒选择入口",
      "需要时再查概念",
      "codex-是什么",
      "权限与安全",
      "agents.md",
      "skills",
      "mcp-plugins",
      "subagents",
      "goal",
      "每页都有真实实例",
      "日常实例",
      "插件实例",
      "skills-仓库实例",
      "权限实例",
      "自动化实例"
    ],
    "install-desktop.html": [
      "安装前先确认三件事",
      "官方入口",
      "账号和组织",
      "仓库准备",
      "安装到第一个任务",
      "第一个任务怎么写",
      "只读入门",
      "小改动入门",
      "第一次不要这样写",
      "看到权限请求时怎么判断",
      "本地服务",
      "联网查询",
      "安装依赖",
      "git-push",
      "真实实例-本指南的-desktop-安装页"
    ],
    "mcp.html": [
      "它是什么",
      "什么时候用-不用",
      "可复制示例",
      "补充内容",
      "最近较火的-mcp-能力",
      "github-全链路",
      "浏览器自动化-playwright",
      "搜索与情报聚合",
      "数据库与知识库查询",
      "设计与协作工具",
      "命令与执行接口",
      "热点功能怎么选",
      "你要写代码但不想查网页",
      "你要做研究复核",
      "你要修复部署问题",
      "最容易踩雷的误区",
      "mcp-适合解决什么问题",
      "github",
      "设计工具",
      "数据和文档",
      "使用-mcp-前的-5-个问题",
      "mcp-安全调用模板",
      "真实实例-只读核对-pages-状态"
    ],
    "permissions.html": [
      "它是什么",
      "codex-desktop-权限等级一览",
      "read-only",
      "workspace-write",
      "auto-建议默认",
      "auto-review",
      "什么时候批准",
      "可复制示例",
      "补充内容",
      "审批决策矩阵",
      "通常可以批准",
      "需要追问",
      "默认拒绝",
      "你可以这样要求-codex-申请权限",
      "secret-和生产数据规则",
      "真实实例-验证-github-pages-发布"
    ],
    "prompt-guidance.html": [
      "先分清三层",
      "官方指南到底在说什么",
      "把建议翻成-codex-任务合同",
      "refine-user-prompt-是什么",
      "四种执行模式",
      "模型与思考强度怎么选",
      "润色不会自动扩大权限",
      "安装和调用",
      "真实实例-润色后执行文档更新",
      "什么时候不该用"
    ],
    "research.html": [
      "从-idea-到可审查证据",
      "research-brief",
      "closest-work",
      "novelty-gate",
      "experiment-plan",
      "auto-review",
      "writing-boundary",
      "每个阶段应该产出什么",
      "research_brief.md",
      "idea_report.md",
      "实验日志",
      "auto_review.md",
      "图表索引",
      "claim-ledger",
      "可复制学术提示词",
      "启动-research-pipeline",
      "严格审稿",
      "进入和退出条件",
      "进入条件",
      "推进条件",
      "退出条件",
      "stop-conditions",
      "写作前检查",
      "真实实例-长上下文-kv-cache-pruning-idea",
      "输入",
      "先读",
      "应动文件",
      "验证",
      "最终回答",
      "失败停止"
    ],
    "resources.html": [
      "中文术语对照",
      "官方资料优先",
      "chatgpt-desktop-app",
      "permissions-docs",
      "scheduled-tasks-docs",
      "browser-docs",
      "integrated-terminal-docs",
      "skills-plugins-docs",
      "gpt-5p6-prompt-guidance",
      "agents-md-docs",
      "subagents-docs",
      "mcp-docs",
      "worktrees-docs",
      "cli-docs",
      "ide-docs",
      "cloud-docs",
      "changelog-docs",
      "record-replay-docs",
      "旧主题的站内对应路径",
      "best-practices",
      "workflows",
      "github-integration",
      "review",
      "本指南内部资料",
      "安装页",
      "readme",
      "context",
      "历史流程图",
      "高-stars-skills-仓库介绍",
      "compound-engineering-plugin",
      "gpt-5.6-提示词与-refine-user-prompt",
      "真实实例-资料如何进入页面内容"
    ],
    "skills-repositories.html": [
      "先按任务-fit-选仓库",
      "30-秒选择表",
      "先看案例证据等级",
      "codex-cli-生态-top-10",
      "compound-engineering",
      "能力",
      "最适合",
      "安装路径",
      "案例-从需求到-pr-1",
      "mattpocock-skills",
      "能力-2",
      "最适合-2",
      "启用路径",
      "案例-先建立上下文-再-grill",
      "academic-research-skills-codex",
      "能力-3",
      "最适合-3",
      "安装路径-2",
      "场景-先做-novelty-与最小实验矩阵",
      "aris-auto-claude-code-research-in-sleep",
      "能力-4",
      "最适合-4",
      "启用路径-2",
      "场景-夜间循环保留人工闸门",
      "taste-skill",
      "ian-xiaohei-illustrations",
      "awesome-chatgpt-prompts-zh",
      "refine-user-prompt",
      "高级用户-按阶段组合-不要一锅端",
      "使用边界",
      "真实实例-历史案例",
      "输入",
      "先读",
      "应动文件",
      "验证",
      "最终回答",
      "失败停止"
    ],
    "skills.html": [
      "它是什么",
      "什么时候用-不用",
      "可复制示例",
      "skill-应该沉淀什么",
      "触发条件",
      "上下文读取",
      "执行流程",
      "输出合同",
      "从-prompt-到-skill-的生命周期",
      "先手写-prompt",
      "提取稳定步骤",
      "加入验证",
      "维护版本",
      "一个实用-skill-模板",
      "真实实例-区分官方指南和第三方-skill"
    ],
    "subagents.html": [
      "它是什么",
      "什么时候用-不用",
      "可复制示例",
      "worktree-subagent-目录隔离和责任隔离",
      "subagent-任务合同",
      "输入",
      "输出",
      "整合",
      "推荐和不推荐的拆法",
      "推荐-并行只读审查",
      "推荐-互不重叠实现",
      "不推荐-共享核心文件",
      "不推荐-外部写操作",
      "bad-split-repaired-split",
      "真实实例-历史复合案例"
    ],
    "workflows.html": [
      "先选工作面-再写任务",
      "安装-desktop",
      "codex-desktop",
      "日常小任务",
      "工程-flow",
      "学术-flow",
      "自动化",
      "skills-仓库选择",
      "compound-engineering",
      "同一任务-小步练到可验收",
      "1.-现象",
      "2.-合同",
      "3.-最小执行",
      "4.-验收请求",
      "v1-只有愿望",
      "v2-补上下文与边界",
      "v3-补验收证据",
      "统一案例模板",
      "坏-prompt-怎么修",
      "帮我优化项目",
      "直接推送",
      "开-subagent-并行做",
      "证据通过-才算-accepted",
      "accepted",
      "not-accepted",
      "先分类失败-再决定回路",
      "用两种终态收口",
      "done-receipt",
      "blocked-receipt",
      "真实实例-从一句反馈选择任务路径",
      "1.-request",
      "2.-context-to-inspect",
      "3.-allowed-change",
      "4.-validation-evidence",
      "5.-final-report",
      "6.-failure-stop"
    ],
    "worktrees.html": [
      "worktree-是什么",
      "什么时候用-不用",
      "在-desktop-中创建",
      "选择-worktree",
      "选择起始分支",
      "提交独立任务",
      "决定继续位置",
      "local-worktree-与-handoff",
      "分支和文件边界",
      "同一分支不能多处-checkout",
      "ignored-文件与-worktreeinclude",
      "恢复与清理",
      "worktree-与-subagent-的区别",
      "可复制示例",
      "真实实例-并行页面修复"
    ]
  },
  "navigation": [
    {
      "label": "开始",
      "pages": [
        "index.html",
        "install-desktop.html",
        "desktop-cli.html"
      ]
    },
    {
      "label": "基础概念",
      "pages": [
        "codex.html",
        "permissions.html",
        "agents-md.html",
        "skills.html",
        "mcp.html",
        "worktrees.html",
        "subagents.html",
        "goal.html"
      ]
    },
    {
      "label": "任务路径",
      "pages": [
        "workflows.html",
        "daily-workflow.html",
        "engineering.html",
        "research.html",
        "automation.html"
      ]
    },
    {
      "label": "扩展与资料",
      "pages": [
        "compound-engineering.html",
        "skills-repositories.html",
        "prompt-guidance.html",
        "resources.html"
      ]
    }
  ],
  "pages": [
    {
      "description": "从一个可验证的小任务开始，并区分 Codex 原生能力与本指南推荐实践。",
      "facts_verified": "2026-07-16",
      "modified": "2026-07-16",
      "nav_label": "首页",
      "path": "index.html",
      "sources": [
        {
          "kind": "official",
          "label": "Codex best practices",
          "url": "https://learn.chatgpt.com/guides/best-practices"
        }
      ],
      "title": "中文 Codex 实战手册"
    },
    {
      "description": "安装 ChatGPT desktop app，并在 Codex 工作面完成首个只读任务。",
      "facts_verified": "2026-07-16",
      "modified": "2026-07-16",
      "nav_label": "安装",
      "path": "install-desktop.html",
      "sources": [
        {
          "kind": "official",
          "label": "ChatGPT desktop app",
          "url": "https://learn.chatgpt.com/docs/app"
        }
      ],
      "title": "安装 Codex Desktop"
    },
    {
      "description": "在 ChatGPT desktop app 的 Codex 工作面使用线程、Browser、Integrated terminal、审批与 diff。",
      "facts_verified": "2026-07-16",
      "modified": "2026-07-16",
      "nav_label": "Desktop",
      "path": "desktop-cli.html",
      "sources": [
        {
          "kind": "official",
          "label": "ChatGPT desktop app",
          "url": "https://learn.chatgpt.com/docs/app"
        },
        {
          "kind": "official",
          "label": "Browser",
          "url": "https://learn.chatgpt.com/docs/browser"
        }
      ],
      "title": "Codex Desktop 操作手册"
    },
    {
      "description": "理解 ChatGPT desktop app 中 Codex 工作面的能力与适用边界。",
      "facts_verified": "2026-07-16",
      "modified": "2026-07-16",
      "nav_label": "Codex",
      "path": "codex.html",
      "sources": [
        {
          "kind": "official",
          "label": "ChatGPT desktop app",
          "url": "https://learn.chatgpt.com/docs/app"
        }
      ],
      "title": "Codex 是什么"
    },
    {
      "description": "理解 Desktop 常见权限模式及底层 sandbox、approval、network 与 secret 边界。",
      "facts_verified": "2026-07-16",
      "modified": "2026-07-16",
      "nav_label": "权限",
      "path": "permissions.html",
      "sources": [
        {
          "kind": "official",
          "label": "Permissions",
          "url": "https://learn.chatgpt.com/docs/permission-modes"
        },
        {
          "kind": "official",
          "label": "Sandbox and approvals",
          "url": "https://learn.chatgpt.com/docs/sandboxing"
        }
      ],
      "title": "权限与安全"
    },
    {
      "description": "理解 AGENTS.md 发现链并写清项目规则、边界和验证命令。",
      "facts_verified": "2026-07-16",
      "modified": "2026-07-16",
      "nav_label": "AGENTS.md",
      "path": "agents-md.html",
      "sources": [
        {
          "kind": "official",
          "label": "AGENTS.md",
          "url": "https://learn.chatgpt.com/docs/agent-configuration/agents-md"
        }
      ],
      "title": "AGENTS.md"
    },
    {
      "description": "用 $skill-name mention 选择和使用 Codex skills。",
      "facts_verified": "2026-07-16",
      "modified": "2026-07-16",
      "nav_label": "Skills",
      "path": "skills.html",
      "sources": [
        {
          "kind": "official",
          "label": "Build skills",
          "url": "https://learn.chatgpt.com/docs/build-skills"
        },
        {
          "kind": "official",
          "label": "Skills & Plugins",
          "url": "https://learn.chatgpt.com/docs/skills-and-plugins"
        }
      ],
      "title": "Skills"
    },
    {
      "description": "区分 MCP servers 与 installable plugins，并管理 tools、resources 和外部能力权限。",
      "facts_verified": "2026-07-16",
      "modified": "2026-07-16",
      "nav_label": "MCP",
      "path": "mcp.html",
      "sources": [
        {
          "kind": "official",
          "label": "MCP",
          "url": "https://learn.chatgpt.com/docs/extend/mcp"
        },
        {
          "kind": "official",
          "label": "Skills & Plugins",
          "url": "https://learn.chatgpt.com/docs/skills-and-plugins"
        }
      ],
      "title": "MCP 与 Plugins"
    },
    {
      "description": "在 Codex Desktop 中用 Worktree 隔离并行任务，并安全地在 Local 与 Worktree 间交接。",
      "facts_verified": "2026-07-16",
      "modified": "2026-07-16",
      "nav_label": "Worktrees",
      "path": "worktrees.html",
      "sources": [
        {
          "kind": "official",
          "label": "Git worktrees",
          "url": "https://learn.chatgpt.com/docs/environments/git-worktrees"
        }
      ],
      "title": "Worktrees"
    },
    {
      "description": "显式传递上下文、拆分写域并由主线程收口 subagent 工作。",
      "facts_verified": "2026-07-16",
      "modified": "2026-07-16",
      "nav_label": "Subagents",
      "path": "subagents.html",
      "sources": [
        {
          "kind": "official",
          "label": "Subagents",
          "url": "https://learn.chatgpt.com/docs/agent-configuration/subagents"
        }
      ],
      "title": "Subagents"
    },
    {
      "description": "理解原生 Goal 与本指南推荐提示词模板的边界。",
      "facts_verified": "2026-07-16",
      "modified": "2026-07-16",
      "nav_label": "Goal",
      "path": "goal.html",
      "sources": [
        {
          "kind": "official",
          "label": "Goal mode and prompting",
          "url": "https://learn.chatgpt.com/docs/prompting#goal-mode"
        }
      ],
      "title": "Goal"
    },
    {
      "description": "根据任务复杂度选择工作流，并用推荐 receipt 实践收口。",
      "facts_verified": "2026-07-12",
      "modified": "2026-07-12",
      "nav_label": "任务",
      "path": "workflows.html",
      "sources": [],
      "title": "任务路径"
    },
    {
      "description": "完成解释、修复、测试和审查，并用推荐 closeout 字段收口。",
      "facts_verified": "2026-07-12",
      "modified": "2026-07-12",
      "nav_label": "日常",
      "path": "daily-workflow.html",
      "sources": [],
      "title": "日常任务 workflow"
    },
    {
      "description": "用用户、编排线程和执行线程组织从需求澄清到验证发布的工程任务。",
      "facts_verified": "2026-07-12",
      "modified": "2026-07-12",
      "nav_label": "工程",
      "path": "engineering.html",
      "sources": [],
      "title": "工程 flow"
    },
    {
      "description": "从研究问题到实验和写作的学术任务路径。",
      "facts_verified": "2026-07-12",
      "modified": "2026-07-12",
      "nav_label": "学术",
      "path": "research.html",
      "sources": [],
      "title": "学术 flow"
    },
    {
      "description": "配置 Scheduled tasks、Scheduled 视图、运行环境与无人值守安全边界。",
      "facts_verified": "2026-07-16",
      "modified": "2026-07-16",
      "nav_label": "定时任务",
      "path": "automation.html",
      "sources": [
        {
          "kind": "official",
          "label": "Scheduled tasks",
          "url": "https://learn.chatgpt.com/docs/automations"
        }
      ],
      "title": "Scheduled tasks（定时任务）"
    },
    {
      "description": "使用 Compound Engineering 插件命令，并约束 /lfg 与无人值守任务边界。",
      "facts_verified": "2026-07-16",
      "modified": "2026-07-16",
      "nav_label": "Compound",
      "path": "compound-engineering.html",
      "sources": [
        {
          "kind": "third_party",
          "label": "Compound Engineering repository",
          "url": "https://github.com/EveryInc/compound-engineering-plugin"
        },
        {
          "kind": "official",
          "label": "Skills & Plugins",
          "url": "https://learn.chatgpt.com/docs/skills-and-plugins"
        }
      ],
      "title": "Compound Engineering plugin"
    },
    {
      "description": "比较第三方 skills 仓库及 Desktop、CLI 与本地安装边界。",
      "facts_verified": "2026-07-16",
      "modified": "2026-07-16",
      "nav_label": "Skills 仓库",
      "path": "skills-repositories.html",
      "sources": [
        {
          "kind": "official",
          "label": "Build skills",
          "url": "https://learn.chatgpt.com/docs/build-skills"
        },
        {
          "kind": "third_party",
          "label": "GitHub codex-cli topic",
          "url": "https://github.com/topics/codex-cli"
        }
      ],
      "title": "Skills 仓库"
    },
    {
      "description": "解读 GPT-5.6 提示词指南，并使用 refine-user-prompt 把原始请求改写成可执行任务合同。",
      "facts_verified": "2026-07-16",
      "modified": "2026-07-16",
      "nav_label": "提示词",
      "path": "prompt-guidance.html",
      "sources": [
        {
          "kind": "official",
          "label": "GPT-5.6 prompting guidance",
          "url": "https://developers.openai.com/api/docs/guides/prompt-guidance-gpt-5p6"
        },
        {
          "kind": "third_party",
          "label": "refine-user-prompt repository",
          "url": "https://github.com/WhoJay0609/refine-user-prompt"
        }
      ],
      "title": "GPT-5.6 提示词与 refine-user-prompt"
    },
    {
      "description": "查找 canonical 官方资料、中文术语对照与本指南维护边界。",
      "facts_verified": "2026-07-16",
      "modified": "2026-07-16",
      "nav_label": "资料",
      "path": "resources.html",
      "sources": [],
      "title": "资料地图"
    }
  ],
  "site": {
    "base_url": "https://whojay0609.github.io/codex-usage-guide/",
    "language": "zh-CN",
    "social_preview": "figures/social-preview.png",
    "title": "Codex 使用指南"
  }
};
