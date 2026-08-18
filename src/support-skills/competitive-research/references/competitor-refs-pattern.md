# 竞品参考库四字段结构（Competitor References Pattern）

> 来源吸收：`prd-competitor-check` 的 `competitor_refs.json` 配置机制——竞品参考库四字段结构（主链接+alt_urls+search_keywords+screenshot）+ 6 模块竞品库组织示例 + 可外部配置，作为 competitive-research 的可选落地能力。
> 定位：竞品调研最耗时的环节是"找对竞品、找对链接"，本技法提供一份结构化、可复用的竞品参考库，按模块组织、四字段兜底，避免每次调研都从零开始搜。
> 触发：当竞品调研需要稳定、可长期复用的竞品来源清单，或需要对标特定业务模块时使用。**按需加载，不设全局闸门**。

## 1. 输入映射

| 外部 skill 输入 | pm-scaffold 对应产物 | 说明 |
|---|---|---|
| 模块名（如"技能商店"） | competitive-research 的调研目标（业务级 vs 功能级） | 路由到对应模块竞品库 |
| `competitor_refs.json` | 竞品来源登记（SRC-ID） | 每个竞品条目 = 一个候选 SRC |
| 外部 refs 文件（--refs-file） | source-handling 的来源替换 | 可外部配置覆盖内置库 |
| 竞品四字段 | Intake 的竞品陈述提取 | 先看主链接/截图说明，再逐字提取 |

> **来源保真**：参考库提供的是"入口"，不是"结论"——竞品的实际陈述仍须按 source-handling 逐字提取并归类 `FACT`/`AI_INFERENCE`。

## 2. 竞品条目四字段结构

每个竞品由以下字段构成（吸收自 `competitor_refs.json`）：

```json
{
  "name": "阿里云百炼平台",
  "url": "https://help.aliyun.com/zh/model-studio",
  "url_type": "官方文档中心",
  "screenshot": "模型广场：网格布局展示 AI 模型卡片...",
  "alt_urls": [
    "https://www.aliyun.com/product/model-studio",
    "https://help.aliyun.com/zh"
  ],
  "search_keywords": "阿里云百炼，阿里云模型工作室，阿里云 AI 市场"
}
```

| 字段 | 含义 | 要求 |
|---|---|---|
| **name** | 竞品名称 | 唯一、可识别 |
| **url** | 主链接 | **官网首页或文档中心首页**，避免深层文档链接（易失效） |
| **url_type** | 链接类型 | 官方首页/文档中心/产品首页/帮助文档 |
| **screenshot** | 界面截图说明 | 详细描述界面布局，供对标时对照 |
| **alt_urls** | 备选链接 | 2-3 个，主链接失效时依次尝试 |
| **search_keywords** | 搜索关键词 | 所有链接失效时用于搜索引擎查找 |

> **链接选择原则**：优先官网首页（如 `https://github.com/marketplace`）→ 其次文档中心首页（如 `https://help.aliyun.com/zh`）→ 避免深层文档链接。

## 3. 6 模块竞品库组织示例（内置配置）

竞品库按业务模块组织，每个模块挂载 2-5 个竞品：

| 模块 | 覆盖竞品 | 链接类型 |
|---|---|---|
| 技能商店 | GitHub Marketplace、VS Code Extensions、阿里云百炼、腾讯 SkillHub、腾讯云 AI 市场 | 官方首页/市场首页 |
| 设备管理 | 华为 eSight、中兴 NetNumen | 产品首页/解决方案 |
| 配置下发 | 华为配置管理、阿里云配置中心 | 产品首页/文档中心 |
| 工单管理 | 华为服务管理、阿里云工单系统 | 产品首页/帮助文档 |
| 权限管理 | 华为权限管理、阿里云 RAM、腾讯云 CAM | 产品首页/文档中心 |
| 批量运维 | 华为运维编排、阿里云运维编排、腾讯云批量计算 | 产品首页/文档中心 |

### 真实字段示例（技能商店模块，吸收自 `competitor_refs.json`）

| 竞品 | 主链接（url） | url_type | 截图说明（screenshot） |
|---|---|---|---|
| GitHub Marketplace | `https://github.com/marketplace` | 官方市场首页 | 列表页：左侧分类筛选，右侧卡片网格展示，支持搜索和排序 |
| VS Code Extensions | `https://marketplace.visualstudio.com` | 官方市场首页 | 扩展列表：左侧分类树，右侧卡片列表，支持评分筛选和排序 |
| 阿里云百炼平台 | `https://help.aliyun.com/zh/model-studio` | 官方文档中心 | 模型广场：网格布局展示 AI 模型卡片，支持按分类、价格、提供商筛选 |
| 腾讯 SkillHub | `https://cloud.tencent.com` | 官网首页 | 云产品列表：卡片式布局，支持搜索和分类浏览 |
| 腾讯云 AI 市场 | `https://cloud.tencent.com/product/aimarket` | 产品首页 | AI 产品列表：网格布局，展示 AI 模型和解决方案，支持按行业筛选 |

> 每个竞品的 alt_urls（2-3 个）与 search_keywords 见 `competitor_refs.json` 原文；本表摘其主干。

## 4. 可外部配置

内置库之外，允许用外部 JSON 覆盖或扩展：

```json
{
  "技能商店": [
    {
      "name": "我的竞品 A",
      "url": "https://competitor-a.com",
      "url_type": "官方首页",
      "screenshot": "竞品 A 的界面说明...",
      "alt_urls": ["https://docs.competitor-a.com"],
      "search_keywords": "竞品 A, Competitor A"
    }
  ]
}
```

- 配置结构：`模块名 → 竞品数组 → 四字段对象`
- 外部文件优先级高于内置配置；缺字段时用内置库对应条目兜底
- 新增竞品后按 link-validation 三层机制验证链接可用性再入库

## 5. 工作流程

1. **定模块**：按调研目标确定业务模块（业务级选大模块，功能级选子模块）。
2. **取库**：从内置配置或外部配置文件取该模块竞品清单。
3. **核入口**：对每条目记录主链接 → alt_urls → search_keywords（供 link-validation 降级）。
4. **登记 SRC**：每个竞品条目分配一个 SRC-ID，记录来源与检索日期。
5. **提取陈述**：按 source-handling 逐字提取竞品功能/定价/定位陈述，不合并两个竞品。
6. **补库**：发现新竞品按四字段结构回写参考库，走 link-validation 验证后再入库。

## 6. 核心硬规则

1. **主链接只放官网/文档中心首页**：深层链接易失效，一律不放主链接位。
2. **四字段缺一不入库**：name/url/screenshot/alt_urls/search_keywords 任一缺失，标 `待补充`，不视为可用条目。
3. **alt_urls 保持 2-3 个且有序**：按优先级排列，降级时依序尝试，找到第一个可用即停。
4. **search_keywords 是最后的兜底**：主链接与备选全失效时才启用，不是默认入口。
5. **外部配置可覆盖内置库**：自定义文件优先，但结构必须一致（模块→数组→四字段）。
6. **入库即验证**：新竞品加入参考库前按 link-validation 跑一次链接检查。

## 7. 边界（Do Not）

- 不把参考库当结论库——库只提供入口，竞品陈述仍须逐字提取与标注。
- 不用深层文档链接做主链接——即使内容更对口，寿命不如首页。
- 不为凑数量加竞品——每模块 2-5 个深度条目优于 20 个一行条目。
- 不合并竞品陈述到一行——两个竞品的说法保持分离，保留各自 SRC-ID。
- 不改写截图说明——screenshot 字段记录"界面是什么样"，判断留给对标环节。

## 8. 质量自检清单

- [ ] 每个竞品条目四字段齐全（主链接/alt_urls/search_keywords/screenshot）
- [ ] 主链接均为官网首页或文档中心首页，无深层链接
- [ ] alt_urls 2-3 个且按优先级有序
- [ ] 模块覆盖与调研目标匹配，竞品数量在 2-5 个
- [ ] 每个竞品条目已分配 SRC-ID，来源与检索日期已记录
- [ ] 外部配置结构（模块→数组→四字段）与内置库一致
- [ ] 新增竞品已通过 link-validation 链接检查后入库
- [ ] 竞品陈述按 source-handling 归类（FACT/AI_INFERENCE），未合并来源
