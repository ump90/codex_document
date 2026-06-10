### 生成幻灯片 Deck

Source: [Generate slide decks](https://developers.openai.com/codex/use-cases/generate-slide-decks.md)

操作 pptx 文件，并使用图像生成自动化创建幻灯片。

#### 概览

使用 Codex 直接通过代码编辑幻灯片、生成视觉素材，并逐页应用可重复布局规则，以更新现有演示文稿或构建新 deck。

适合：

- 将笔记或结构化输入转化为可重复 slide decks 的团队。
- 从零创建新的视觉演示。
- 从截图、PDF 或参考演示中重建或扩展 decks。

相关 skill：

- `$slides`：使用 JavaScript、PptxGenJS、捆绑 helpers，以及用于 overflow、overlap 和 font 检查的 render 与 validation scripts 创建和编辑 `.pptx` decks。
- `$imagegen`：生成插图、封面图、图表和幻灯片视觉素材，并匹配同一个可复用视觉方向。

#### 起始提示

**创建新的 slide deck**

```text
使用 $slides 和 $imagegen skills 按以下方式编辑这个 slide deck：

- 如果存在，在每张 slide 的右下角添加 logo.png
- 在 slides X、Y 和 Z 上，将文本移到左侧，并使用图像生成在右侧生成一张插图（style: abstract, digital art）
- 可行时，将文本保留为文本，将简单图表保留为 native PowerPoint charts。
- 添加这些 slides：[describe new slides here]
- 在新 slides 和新文本中使用现有品牌风格（colors、fonts、layout 等）
- 将更新后的 deck 渲染为 slide images，审查输出，并在交付前修复布局问题。
- 交付前运行 overflow 和 font-substitution 检查，尤其是在 deck 很密集时。
- 当你创建一批相关图像时，保存可复用 prompts 或 generation notes。

输出：
- 一份已应用变更的 slide deck 副本
- 关于哪些 slides 被生成、重写或保持不变的说明
```

#### 相关链接

- [图像生成指南](https://developers.openai.com/api/docs/guides/image-generation)

## 介绍

你可以使用 Codex 系统化地操作 PowerPoint decks：使用 Codex 默认附带的 slides system skill，通过 PptxGenJS 创建和编辑 decks，并使用图像生成来为 slides 生成视觉素材。

Skills 可以直接从 Codex app 安装，更多细节请参阅我们的 [skills 文档](48-agent-skills.md)。

你可以从零创建新 decks，描述你想要的内容；但理想工作流是从一个已经存在且已设置好品牌指南的 deck 开始，让 Codex 编辑它。

## 从源 deck 和参考开始

如果 deck 已经存在，请让 Codex 在修改前检查它。

slides system skill 在这里有明确偏好：重建布局前先匹配源文件宽高比；只有当源材料没有定义 deck 尺寸时，才默认使用 16:9。如果参考是截图或 PDF，请让 Codex 先渲染或检查它们，这样它可以视觉比较 slide 几何，而不是猜。

## 保持 deck 可编辑

构建新 slides 时，让 Codex 保持 slides 可编辑：当 slides 包含文本、图表或简单布局元素时，可行时应保持 PowerPoint-native。文本应保持为文本。简单柱状图、折线图、饼图和直方图视觉元素应尽可能保持为 native charts。对于过于自定义、无法用 native slide objects 表达的图表或视觉元素，Codex 可以有意生成或放置 SVG 和 image assets，而不是把整张 slide 栅格化。

例如，如果你想构建一个带插图的复杂时间线，不要生成整张图片，而是让 Codex 分别生成每个插图（使用一组 style prompt 作为参考），把它们放到 slide 上，然后用 native lines 连接。文本和日期也应是 text objects，而不是包含在插图中。

## 有意生成视觉素材

imagegen system skill 已随 Codex 安装，当 slides 需要封面图、概念插图或轻量 diagram，而这些原本需要手工设计时，它最有用。让 Codex 先定义视觉方向，然后在整个 deck 中一致复用该方向。

当多张 slides 需要相关视觉素材时，让 Codex 保存它使用过的 prompts 或 generation notes。这样以后扩展 deck 时更容易保持风格一致，而不必从头开始。

## 明确 slide 逻辑

当 Codex 把每张 slide 都视为一个单独决策时，deck 自动化效果更好。有些 slides 应保留精确文案，有些需要更有力的标题和更清晰结构，有些除了资产清理或格式修复外应基本保持不变。

slides system skill 还附带捆绑的 layout helpers。让 Codex 将这些 helpers 复制到工作目录并复用它们，而不是在每个 deck 中重新实现 spacing、text-sizing 和 image-placement 逻辑。

## 交付前验证

Decks 很容易做到差不多正确，但仍带着被裁剪文本、替代字体或导出后才出现的布局漂移交付。slides system skill 包含脚本，可将 decks 渲染为逐页 PNG、生成快速 montage 供审查、检测超出 slide 画布的 overflow，并报告缺失或被替代的 fonts。

交付最终 deck 前，让 Codex 使用这些检查，尤其是在 slides 密集或边距很紧时。

## 示例想法

这里有一些可以尝试的想法：

### 从零创建新 deck

你可以从零创建新的 slide decks，逐页描述你想要的内容和整体氛围。
如果你有 logos 或 images 等 assets，可以把它们复制到同一个文件夹中，方便 Codex 访问。

### Deck 模板更新

你可以定期（每周、每月、每季度等）用新内容更新 deck 模板。
如果你经常这样做，请创建类似 `guidelines.md` 的文件，定义 deck 的内容和结构以及应如何更新。

将它与其他 skills 结合，从你偏好的数据来源获取信息。

例如，如果你需要向利益相关者做季度更新，可以用新数字和洞察更新 deck 模板。

### 调整现有 deck

如果你已经构建了一个 deck，但想调整它以修复间距、文本未对齐或其他布局问题，可以让 Codex 修复它。
