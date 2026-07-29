# 输出真实样例

三种典型查询的完整"用户问题 → 最终输出"样例，输出格式规则见 SKILL.md
「给用户的输出格式」一节。

1. [宽问题 → 精选 + 时间窗](#样例-1宽问题--精选--时间窗)（列表式、多 category 分组 + 全局编号）
2. [明确说"日报" → daily](#样例-2明确说日报--daily)（日报式）
3. [公司关键词 → q 搜索](#样例-3公司关键词--q-搜索)（列表式、按 category 分组）

---

## 样例 1：宽问题 → 精选 + 时间窗

> 用户：今天 AI 圈有什么？

**AI HOT 最近 24 小时精选**

按发布时间倒序。

## 模型发布/更新

1. **Cartesia 发布 Sonic 3.5 与 Ink 2 实时语音模型** — X：Testing Catalog (@testingcatalog)
   6/16 14:42 北京时间
   Cartesia 推出 Sonic 3.5 和 Ink 2 两个模型，作为单一实时语音栈，分别负责文本转语音和语音转文本。Ink 2 在 Artificial Analysis 的流式语音转文字排行榜上排名第一。Sonic 3.5 在实时文本转语音中位列榜首，首音频延迟约 82ms。Cartesia 成为目前唯一同时拥有 #1 听与说模型的提供商。
   https://x.com/testingcatalog/status/2066773392527655252

## 产品发布/更新

2. **Google Cloud 推出 OKF v0.1：供应商中立的 Markdown 规范，为 AI 智能体提供结构化上下文** — MarkTechPost（RSS）
   6/16 16:18 北京时间
   Google Cloud 发布 Open Knowledge Format （OKF） v0.1，一种供应商中立的 Markdown 规范，为 AI 智能体提供结构化上下文知识。OKF 将知识表示为带 YAML 前置元数据的 markdown 文件目录，每个概念对应一个文件，通过 `type`、`title`、`description` 等少量保留字段实现互操作。无需专有服务、SDK 或运行时，目录可托管在 GitHub、以 tarball 传输或挂载到任意文件系统。OKF 旨在解决组织内部知识碎片化问题--表结构、指标定义、runbook 等散落在不同 catalog 和 wiki 中，各厂商方案互不兼容。遵循最少意见原则，只强制 `type` 字段，生产者和消费者可独立实现。使用场景包括数据团队将 BigQuery 表定义导出为代码、为智能体存储 incident runbook、跨组织知识交换等。
   https://www.marktechpost.com/2026/06/16/google-cloud-introduces-open-knowledge-format-okf-a-vendor-neutral-markdown-spec-for-giving-ai-agents-curated-context

3. **AI 版支付宝官宣开启邀测：右滑打开"阿宝"，官方放出 100 个邀请码** — IT之家（RSS）
   6/16 10:39 北京时间
   支付宝今日开启 AI 版邀测，用户可右滑进入新版界面，在对话框或语音中输入指令，由"阿宝"助手代办事项。以查询公积金为例，阿宝自动匹配对应小程序和服务入口，用户点击确认即可完成，将多步跳转折叠为一句指令。所有涉及资金变动和支付的环节均需用户本人确认。首批放出 100 个邀请码。
   https://www.ithome.com/0/964/691.htm

## 行业动态

4. **美国司法部援引国家安全为xAI未经许可的燃气轮机辩护** — The Decoder：AI News（RSS）
   6/16 21:23 北京时间
   美国司法部在一份驳回诉讼的动议中称，xAI的聊天机器人Grok对军事行动至关重要，以此为其在密西西比州Southaven的Colossus 2设施运行未经许可的燃气轮机辩护。NAACP已提起诉讼，指控xAI的燃气轮机数量从4月的27台增至57台，导致氮氧化物排放飙升111%。国防部首席数字与人工智能官Cameron Stanley表示，Grok是支持机密和绝密网络军事任务的四款AI模型之一，包括近期针对伊朗的打击。
   https://the-decoder.com/doj-invokes-national-security-to-defend-xais-unpermitted-gas-turbines-in-naacp-lawsuit

5. **2025年OpenAI亏损额激增近8倍，支出高达340亿美元** — Hacker News 热门（buzzing.cc 中文翻译）
   6/16 21:01 北京时间
   据Hacker News热门文章，OpenAI在2025年亏损额激增近8倍，年度总支出达到340亿美元。原文来自wheresyoured.at的独家财务分析报道，该信息在Hacker News上获得超过100个点赞。
   https://www.wheresyoured.at/exclusive-openai-financials

6. **SpaceX 以 600 亿美元股票收购 AI 编程公司 Cursor** — TechCrunch：AI（RSS）
   6/16 19:21 北京时间
   SpaceX 在历史性 IPO 数天后，同意以 600 亿美元股票收购 AI 编程初创公司 Cursor，旨在帮助其围绕 xAI 构建的 AI 部门追赶主要 AI 实验室。此前 Cursor 正接近完成一轮 20 亿美元融资，估值 500 亿美元，投资方包括 Andreessen Horowitz、Thrive 和 Nvidia。SpaceX 在 IPO 期间向投资者表示，其 AI 产品可寻址市场达 26 万亿美元。交易预计于今年第三季度完成。
   https://techcrunch.com/2026/06/16/spacex-to-acquire-cursor-for-60b-in-stock-days-after-blockbuster-ipo

7. **DeepSeek 完成首轮外部融资，估值超 500 亿美元** — The Decoder：AI News（RSS）
   6/16 17:40 北京时间
   中国 AI 初创公司 DeepSeek 完成首轮外部融资，募资超 500 亿元人民币（约 74 亿美元），估值超 500 亿美元。投资结构特殊：多数投资者将资金投入 CEO 梁文锋管理的有限合伙企业，无投票权且锁定期五年；仅国资 AI 基金直接投资并保留投票权。创始人梁文锋个人投入约 200 亿元，腾讯和宁德时代为主要外部投资者。梁文锋表示优先基础 AI 研究与 AGI 开发，将继续开源。DeepSeek 去年初凭 V3、R1 模型获全球关注，今年 4 月发布运行于华为芯片的最大开源权重模型 V4，并将 V4 Pro 永久折扣 75%，输入价格约为 OpenAI GPT-5.5 的 1/11，输出价格约为 1/35。
   https://the-decoder.com/deepseek-takes-outside-money-for-the-first-time-at-a-50-billion-valuation

## 论文研究

8. **伯克利RDI发布Agents' Last Exam基准** — Berkeley RDI：Blog（AI 安全与评测）
   6/16 09:59 北京时间
   2026年6月，伯克利RDI发布Agents' Last Exam（ALE）基准，包含1，500余项源于真实工作的任务，覆盖55个非体力职业。对Fable 5、GPT-5.5、Composer 2.5等前沿智能体的测评显示：在最困难层级成功率均为0%；整体任务表现接近，但单任务成本差异巨大（Fable 5约$15.70，GPT-5.5约$3.80，Composer 2.5约$1.33）。CLI子集ALE-CLI最佳通过率仅25.2%。主要失败模式是智能体未验证输出即宣称完成。数据集、代码及CLI子集已开源。
   https://rdi.berkeley.edu/blog/agents-last-exam

## 技巧与观点

9. **WorkBuddy日活飙升至行业第二的3-4倍，非技术用户涌入** — 公众号：数字生命卡兹克
   6/16 20:42 北京时间
   从3月至今，WorkBuddy日活用户数已达行业第二名的3-4倍，用户不再限于开发者，大量HR、运营、行政等非技术岗位也在使用。其企业版和项目功能进一步扩展了Agent办公场景。同期，Trae Work、QoderWork、Kimi Work等产品纷纷改名或出新，争夺市场。腾讯云认为这可能是十年一遇的机遇。
   https://mp.weixin.qq.com/s/iAgbUzPrsbpqvu4s2XiH0g

10. **毕业生陷入AI检测荒诞循环：手写摘要被判99%AI率，AI写部分0%** — 公众号：数字生命卡兹克
   6/16 10:06 北京时间
   当前毕业生面临论文AIGC率检测荒诞困境。学生手写摘要被判定99%AI率，纯AI写部分却为0%。学校要求AIGC率不超40%，学生用Claude反复修改并花上百元检测费（维普20元/篇，知网/万方2元/千字符），最终降至36.1%。答辩时老师要求改回学术表达，AI率回升至37.21%。同一论文在不同平台检测结果差异巨大（48%、44%、59%）。部分平台提供降重收费服务，少数学校已改用AI使用声明表替代一刀切检测。
   https://mp.weixin.qq.com/s/DRzNIiojGLO-iqqPyJ7f8Q

---

## 样例 2：明确说"日报" → daily

> 用户：看一下 AI 日报

**AI HOT 日报 · 2026-06-16**

## 模型发布/更新

1. **MiniMax 开源 M3 模型权重及 MSA 技术论文** — 公众号：MiniMax（稀宇科技）
   MiniMax 上周五开源了 428B 总参数、23B 激活参数的 M3 模型权重，同步发布 MSA（MiniMax Sparse Attention）技术论文，该架构显著降低长上下文计算成本。M3 是首个从预训练阶段就进行文本、图像等多模态交错混合训练的开源模型。发布两周后，M3 在 Artificial Analysis 综合智能指数、GDPval-AA 排行榜均获开源模型第一，Code Arena WebDev 跻身帕累托最优序列，Vals.AI 榜单居国产模型首位。输出速度已从约 30 TPS 提升至约 80 TPS，计划再提速 30–40%；Token Plan 后台新增调用量看板。
   https://mp.weixin.qq.com/s/AW6L89QZkwN-jD27hQ84ww

2. **下一代投机解码：DFlash 与 Spec V2** — LMSYS：Blog（Chatbot Arena 团队）
   Z Lab、Modal 与 SGLang 团队联合发布 DFlash 投机解码模型和 SGLang 的默认 Spec V2 引擎。DFlash 采用块扩散+KV 注入并行生成整块 draft token，在 Qwen 3.5 397B-A17B（BF16）的 HumanEval 数据集上、并发 1 时吞吐量达到基线的 4.3
   https://www.lmsys.org/blog/2026-06-15-next-generation-speculative-decoding-dflash-v2

## 产品发布/更新

3. **Flash-KMeans：IO感知的精确K-Means，在GPU上比FAISS快200倍以上** — MarkTechPost（RSS）
   UC Berkeley与UT Austin团队开源Flash-KMeans（Apache 2.0，`pip install flash-kmeans`），精确实现标准Lloyd's k-Means，通过重构GPU数据流而非改变数学或近似来提速。在NVIDIA H200上，端到端速度比最佳基线快17.9×，比cuML快33×，比FAISS快200×以上。其FlashAssign核避免物化完整N×K距离矩阵，将IO复杂度从O(NK)降至O(Nd+Kd)，单核加速最高21.2×；Sort-Inverse Update核通过排序聚类ID减少原子争用，单核加速最高6.3×。支持out-of-core处理，在1B数据点、K=32768时单次迭代…
   https://www.marktechpost.com/2026/06/15/meet-flash-kmeans-an-io-aware-exact-k-means-that-runs-over-200x-faster-than-faiss-on-gpus

4. **Grok Build 推出 Agent Dashboard 管理多个编码会话** — xAI：News（网页）
   xAI 为 Grok Build 推出 Agent Dashboard，提供单一屏幕管理多个编码会话。仪表板按状态分组（等待输入、工作中、空闲），每行显示状态标记、名称、分支、权限模式和当前操作。选中会话可打开 peek 面板查看最新输出并直接回复，等待输入的会话支持用箭头键或数字键选择选项。底部输入框用于分派新会话，支持设置模型、启动计划模式或自动批准编辑。通过 `grok dashboard`、`/dashboard` 或 `Ctrl+\` 打开，关闭后会话继续运行，重新打开即可恢复。
   https://x.ai/news/agent-dashboard

5. **Meta 在 Facebook 上线"AI Mode"，基于平台公开信息合成答案** — TechCrunch：AI（RSS）
   Meta 宣布在 Facebook 推出"AI Mode"搜索功能，利用 Meta AI 从公开帖子（含群组和 Reels）提取信息并合成答案，用户可用自然语言提问获得摘要。同时新增视频拼贴剪辑、过渡效果及 AI 照片预设（可更换服装、发型和配饰），体育迷可在 Stories 中点击"AI Edit"虚拟穿上队服。这些更新延续了此前动态头像、Marketplace 自动回复和创作者 AI 助手的部署节奏。此外，Meta 近期启动了 Facebook、Instagram 和 WhatsApp 的全球订阅计划（每月 3.99 美元起），更多 AI 订阅层级正在规划中。
   https://techcrunch.com/2026/06/15/metas-new-ai-mode-on-facebook-pulls-from-public-info-across-its-platforms

6. **6倍速！Kimi K2.7 Code 高速版已上线** — 公众号：月之暗面（Kimi）
   Kimi K2.7 Code 高速版上线，与普通版为同一模型，输出速度约 5-6 倍，常规编程场景约 180 Token/s，短上下文可达 260 Token/s。API 定价为普通版 2 倍，模型 ID：kimi-k2.7-code-highspeed。Kimi Code Plan 用户可通过「抢先体验计划」使用，用量消耗为普通版 3 倍。使用须开启思考模式，关闭会报错或回退至 K2.6。庆祝发布，Kimi API 开放平台推出为期三周充赠活动，充值 500 元及以上享 20%-30% 代金券。相比 K2.6，K2.7 Code 在长上下文编程指令遵循、长程任务性能提升，平均 token 消耗减少 30%，内部基准测试显著提升。普…
   https://mp.weixin.qq.com/s/p87ebkY1xqKtkGZ2N3DGSw

7. **OpenRouter新增免费模型gpt-oss-20b和Gemma4 26B** — X：OpenRouter (@OpenRouter)
   OpenRouter 上新增免费容量，由 @eigenlabs 的 Darkbloom 提供：gpt-oss-20b 和 Gemma 4 26B。 今天就开始使用这些模型吧 ↓
   https://x.com/OpenRouter/status/2066585705581797616

8. **GitHub 发布新开源数据集，加速多语言 AI 研究与开发** — GitHub Blog
   GitHub 在 CC0-1.0 许可下发布了一个仓库级数据集，涵盖多语言开发者内容，包括 README、issue 和 pull request。该数据集旨在帮助研究者和开发者发现并利用跨语言的技术文档与社区讨论，以推动多语言 AI 的构建与优化。
   https://github.blog/ai-and-ml/llms/accelerating-researchers-and-developers-building-multilingual-ai-with-a-new-open-dataset

9. **Claude Code v2.1.178 发布** — Claude Code：GitHub Releases（RSS）
   本次更新新增 `Tool(param:value)` 语法用于权限规则匹配工具输入参数；嵌套 `skills` 目录中的技能自动加载，名称冲突时以 `<dir>:<name>` 形式保留；嵌套 `agent`、`workflow`、`output-style` 冲突时取最近目录。改进自动模式下子 agent 生成前的分类器评估；`/doctor` 采用扁平树布局；工作流提示词高亮为紫色闪烁，仅触发显式短语；`/bug` 提交前需填写描述。修复了 CLI 继承过期 WebSocket/OAuth 文件描述符导致的崩溃、Chrome 中 OAuth token 账号不匹配导致连接失败、子 agent 转录显示工具结果、后台恢复不从头重启…
   https://github.com/anthropics/claude-code/releases/tag/v2.1.178

## 行业动态

10. **Salesforce以36亿美元收购AI客服平台Fin** — TechCrunch：AI（RSS）
   Salesforce宣布以36亿美元收购AI客服平台Fin（前身为Intercom）。Fin提供可跨实时聊天、WhatsApp、短信、电话、Slack等多渠道解决客户问题的AI智能体。Salesforce计划利用Fin的技术和团队增强其企业级Agentforce平台，该平台允许企业构建自定义AI智能体以自动化任务。交易预计在Salesforce 2027财年第四季度（即2027年初）完成。Fin联合创始人兼CEO Eoghan McCabe将继续担任CEO，研发负责人Des继续领导研发。
   https://techcrunch.com/2026/06/15/salesforce-acquires-ai-customer-service-platform-fin-for-3-6b

11. **Nvidia 加入 AI 债务热潮，发行 200 亿美元债券** — The Decoder：AI News（RSS）
   Nvidia 计划通过自 2021 年以来的首次债券发行筹集至少 200 亿美元，消息援引知情人士透露。此举标志着 Nvidia 加入 AI 领域的债务融资热潮。
   https://the-decoder.com/nvidia-joins-ai-debt-boom-with-20-billion-bond-sale

12. **Cloudflare 引入 Ensemble AI 团队，加速 AI 基础设施研发** — Cloudflare Blog
   Cloudflare 宣布 Ensemble AI 团队关键成员加入，以加速 AI 基础设施研发。Ensemble 专注于模型压缩与高效推理，开发了 NdLinear（可直接替换 Transformer 标准线性层并保持多维激活结构）和 NdLinear-LoRA（降低大模型微调所需可训练参数）。这些技术与量化等方法互补，旨在降低大语言模型和多模态架构的内存、计算与部署开销。Cloudflare 将把 Ensemble 的成果整合到 Workers AI 平台，通过全球网络与 serverless GPU 推理服务，进一步提升推理效率、GPU 利用率和部署经济性。
   https://blog.cloudflare.com/ensemble-ai-talent-joins-cloudflare

13. **xAI 宣布 Grok 集成至 Warp 终端开发环境** — xAI：News（网页）
   xAI 宣布与 Warp 集成，Warp 是一个基于终端的智能体开发环境，拥有近百万开发者。用户可使用 Grok 或 X Premium 订阅在 Warp 中访问 Grok 模型，包括驱动 Grok Build CLI 的 `grok-build-0.1` 模型。设置方式：下载 Warp，在 Agent 设置页连接 SuperGrok 订阅，切换至 `grok-build-0.1` 模型。更多智能体与集成即将推出。
   https://x.ai/news/grok-warp

## 技巧与观点

14. **Skydio CEO Adam Bry：硅谷不应为无人机使用画红线** — The Verge：AI（RSS）
   Skydio是美国最大的无人机制造商，主攻公共安全、军事、能源、基建巡检等企业市场。CEO Adam Bry表示，特朗普政府去年底禁止中国产无人机后，廉价消费级无人机几乎消失，Skydio产品成为主要替代方案。公司认为无人机正从工具转向自主基础设施——通过机库、远程操控和软件整合实现规模化应用，AI在其中扮演关键角色。访谈还涉及Skydio与军方合作的态度，以及自主技术如何带动公司扩张。
   https://www.theverge.com/podcast/949195/skydio-ceo-adam-bry-autonmous-drones-china-red-lines-military

15. **AI裁员浪潮成为火药桶** — TechCrunch：AI（RSS）
   今年科技公司已累计裁员约15万人，日均974人，速度比去年快44%；上月裁员近4万创两年新高，AI连续三个月被列为裁员首要原因。Block近半数员工被裁后，CEO Jack Dorsey否认AI是根源，Marc Andreessen则称AI只是"银弹借口"。Uber裁撤23%人事部门，但此前CTO透露AI编码预算四个月内耗尽。与此同时，AI芯片商Cerebras上市首日市值达670亿美元，SpaceX上市市值2.1万亿美元，Anthropic和OpenAI估值均约1万亿美元。Meta在扎克伯格购入1.7亿美元豪宅后宣布裁员8000人。民调显示65%选民认为中产阶级生活遥不可及，76%美国人将生活成本列为首要经济问题。
   https://techcrunch.com/2026/06/15/the-ai-layoff-wave-is-becoming-a-powder-keg

16. **AI 应用黄金时代已至：Fable 被禁、Nadella 的护城河论点与 Salesforce 收购 Fin** — Tomer Tunguz 博客（VC 分析）
   美国政府关闭 Anthropic 的 Fable 访问，开源和本地模型成必备；Satya Nadella 主张 AI 生态护城河应是人类专业知识和模型外围系统；Salesforce 以 36 亿美元收购 Fin（前 Intercom），Fin 利用开源模型实现性价比。这三件事标志 AI 应用进入黄金时代。构建 AI 应用的难点：在 Kimi K2.6、Qwen 3.6 27b、GLM 5.1 等不同特性模型中选择；设计智能体系统的 hill-climbing 循环；持续评估模型+循环性能以最大化 token 预算中的智能。掌握这三项技能的公司将主导这一时代。
   https://www.tomtunguz.com/golden-age-of-applications

17. **GitHub Copilot CLI 初学者指南：常用斜杠命令概览** — GitHub Blog
   GitHub Copilot CLI 为初学者提供了常用斜杠命令的概述，帮助用户通过命令控制终端中的 AI 智能体。
   https://github.blog/ai-and-ml/github-copilot/github-copilot-cli-for-beginners-overview-of-common-slash-commands

---

## 样例 3：公司关键词 → q 搜索

> 用户：OpenAI 最近有什么动态？

**AI HOT — OpenAI 相关动态**

按发布时间倒序。

## 产品发布/更新

1. **OpenAI Codex 推出速率重置攒存功能** — X：OpenAI (@OpenAI)
   6/12 08:11 北京时间
   我们听说您希望能在自己方便的时候使用 Codex 速率限制重置。 从今天起，我们开始推出将速率限制重置保留到以后使用的功能。 我们从 Go、Plus、Pro 和 Business 用户开始，每人提供一次免费重置：
   https://x.com/OpenAI/status/2065225362544726371

## 行业动态

2. **2025年OpenAI亏损额激增近8倍，支出高达340亿美元** — Hacker News 热门（buzzing.cc 中文翻译）
   6/16 21:01 北京时间
   据Hacker News热门文章，OpenAI在2025年亏损额激增近8倍，年度总支出达到340亿美元。原文来自wheresyoured.at的独家财务分析报道，该信息在Hacker News上获得超过100个点赞。
   https://www.wheresyoured.at/exclusive-openai-financials

3. **DeepSeek 完成首轮外部融资，估值超 500 亿美元** — The Decoder：AI News（RSS）
   6/16 17:40 北京时间
   中国 AI 初创公司 DeepSeek 完成首轮外部融资，募资超 500 亿元人民币（约 74 亿美元），估值超 500 亿美元。投资结构特殊：多数投资者将资金投入 CEO 梁文锋管理的有限合伙企业，无投票权且锁定期五年；仅国资 AI 基金直接投资并保留投票权。创始人梁文锋个人投入约 200 亿元，腾讯和宁德时代为主要外部投资者。梁文锋表示优先基础 AI 研究与 AGI 开发，将继续开源。DeepSeek 去年初凭 V3、R1 模型获全球关注，今年 4 月发布运行于华为芯片的最大开源权重模型 V4，并将 V4 Pro 永久折扣 75%，输入价格约为 OpenAI GPT-5.5 的 1/11，输出价格约为 1/35。
   https://the-decoder.com/deepseek-takes-outside-money-for-the-first-time-at-a-50-billion-valuation

4. **五角大楼将大部分日常AI工作流从Anthropic转移，目标9月前完全切断** — X：阿易 AI Notes (@AYi_AInotes)
   6/16 08:30 北京时间
   五角大楼宣布已将超2/3日常AI工作流从Anthropic转移，目标9月前清零。起因是年初五角大楼要求Anthropic签署协议允许Claude用于大规模监控和全自动武器，CEO Dario Amodei以模型不可靠为由拒绝。五角大楼将其列为"供应链风险"，起诉未果。OpenAI调整立场获得订单。Polymarket预测6月底前和解概率仅9%。此事件凸显AI公司需在原则与政府合作间抉择。
   https://x.com/AYi_AInotes/status/2066679835607412846

5. **OpenAI 推出合作伙伴网络 OpenAI Partner Network** — OpenAI：官网动态（RSS · 排除企业/客户案例）
   6/15 01:00 北京时间
   OpenAI 宣布推出 OpenAI Partner Network，并投资 1.5 亿美元支持全球合作伙伴构建、销售和交付 AI 解决方案。该计划设立 Select、Advanced、Elite 三级合作伙伴层级，提供 Codex、网络安全、智能体等专业方向认证，并试点 Forward Deployed Experts 项目以支持复杂企业部署。目标在 2026 年底前培训认证 30 万名顾问。案例显示，Paychex 借助 Bain 和 OpenAI 的方案将等待时间降低 80%，人工审核时间减少 30%。
   https://openai.com/index/introducing-openai-partner-network

## 技巧与观点

6. **AI裁员浪潮成为火药桶** — TechCrunch：AI（RSS）
   6/15 15:25 北京时间
   今年科技公司已累计裁员约15万人，日均974人，速度比去年快44%；上月裁员近4万创两年新高，AI连续三个月被列为裁员首要原因。Block近半数员工被裁后，CEO Jack Dorsey否认AI是根源，Marc Andreessen则称AI只是"银弹借口"。Uber裁撤23%人事部门，但此前CTO透露AI编码预算四个月内耗尽。与此同时，AI芯片商Cerebras上市首日市值达670亿美元，SpaceX上市市值2.1万亿美元，Anthropic和OpenAI估值均约1万亿美元。Meta在扎克伯格购入1.7亿美元豪宅后宣布裁员8000人。民调显示65%选民认为中产阶级生活遥不可及，76%美国人将生活成本列为首要经济问题。
   https://techcrunch.com/2026/06/15/the-ai-layoff-wave-is-becoming-a-powder-keg

7. **白宫AI监管决定被指偏袒OpenAI与亚马逊** — Gary Marcus：The Road to AI We Can Trust（RSS）
   6/15 00:15 北京时间
   白宫周五做出的AI监管决定被指偏袒OpenAI、亚马逊等企业，同时对Anthropic施压不足24小时，缺乏透明度和事实依据。Gary Marcus、Dean W Ball及卡托研究所Kevin Frazier等专家指出，这种由少数人闭门快速决策的做法带有腐败嫌疑，可能促使其他国家加速发展"主权AI"甚至中国AI，并导致美国人才流失。Anthropic声明称政府应在法定程序中基于技术事实阻止不安全部署，而非当前方式。Marcus呼吁建立独立机构负责AI监管，确保公平、清晰、基于证据的执行。
   https://garymarcus.substack.com/p/what-washington-must-do

8. **Anthropic 上市前夕** — X：小互 (@xiaohu)
   6/14 10:56 北京时间
   Anthropic CEO Dario Amodei透露内部模型Mythos有上千漏洞，能黑银行、窃取国家机密；预言AI一到五年内砍掉一半入门级白领工作；称Claude已被美军用于对伊朗战争，涉及女校150人死亡拷问；解释离开OpenAI因信任崩塌；回怼黄仁勋末日营销指控；给出文明崩溃概率10%-25%。
   https://x.com/xiaohu/status/2065991805238497732

9. **SemiAnalysis 洞察 Token 经济：200 美元 AI 订阅榨出 70 倍用量** — IT之家（RSS）
   6/13 14:09 北京时间
   SemiAnalysis 购买了 Anthropic 和 OpenAI 的全部订阅方案，模拟高强度编码任务直至触及每周上限。月费 200 美元的 Claude Max 20x 方案，按 API 价格换算最高可消耗约值 8000 美元的 token；ChatGPT Pro 20x 方案对应最高约值 14000 美元的 token。用户通过订阅可获取 40 至 70 倍的 API 价值，该机构指出这种价格体系在重度用户持续榨满上限后可能难以长期维持。
   https://www.ithome.com/0/963/834.htm

10. **OpenAI 推出面向新时代工作的新 Academy 课程** — OpenAI：官网动态（RSS · 排除企业/客户案例）
   6/12 18:00 北京时间
   OpenAI 发布三门 Academy 课程，帮助用户掌握实用 AI 技能、创建可重复工作流，并在日常工作中应用 AI 智能体。
   https://openai.com/index/academy-courses-applying-ai-at-work
