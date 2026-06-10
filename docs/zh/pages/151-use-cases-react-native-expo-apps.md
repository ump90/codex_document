### 使用 Expo 构建 React Native apps

Source: [Build React Native apps with Expo](https://developers.openai.com/codex/use-cases/react-native-expo-apps.md)

用专用 plugin 从移动 app 想法走到可运行的 Expo app。

#### 概览

使用 Codex 搭配 Expo plugin scaffold React Native apps，遵循 Expo Router 和 Expo-native package conventions，先用 Expo Go 快速测试，并且只在 app 需要时才转向 dev clients 或 EAS builds。

适合：

- 希望先用 Expo prototype 或发布 React Native app，再进入 native IDE workflows 的开发者。
- 需要 Codex 遵循 Expo conventions 来处理 routing、UI、package installs、builds 和 deployment 的 Expo Router projects。
- 需要把 web app 迁移为 mobile app 的开发者。

相关 skill：

- `expo`：使用 Expo 官方 skills，处理 Expo Router UI、native-feeling components、data fetching、dev clients、deployment、upgrades、modules 和 Codex Run action wiring。

#### 起始提示

**构建 Expo app**

```text
使用 Expo plugin，为这个想法构建一个 React Native app with Expo：

[describe the app idea, target users, and the main workflow]

要求：
- 从 Expo Router 和 Expo-native project conventions 开始。
- 在创建 custom build 之前，先尝试 `npx expo start` 和 Expo Go。
- 对 Expo packages 使用 `npx expo install`，保持 dependencies compatible。
- 对 navigation、forms、lists、empty states 和 loading states 使用 native-feeling UI patterns。

交付：
- working app slice
- run command
- 你使用的 verification path，包括 Expo Go、device、simulator、dev client 或 EAS
```

建议使用中等推理强度。

#### 技术栈建议

| 需求 | 推荐默认项 | 原因 |
| --- | --- | --- |
| Mobile framework | [Expo](https://expo.dev/) 和 [React Native](https://reactnative.dev/) | Expo 给 Codex 一条 managed React Native path，支持快速迭代、compatible packages 和 deployment tooling。 |
| Routing | [Expo Router](https://docs.expo.dev/router/introduction/) | Expo Router 让 navigation 保持 file-based 且可预测，帮助 Codex 添加 screens 和 flows，而不需要发明自定义 routing layer。 |

#### 从 Expo Go 开始

当你希望 Codex 从 mobile-app idea 走到已测试的 React Native app 时，Expo 是很强的默认选择。有用的循环是先运行 `expo start`，然后在设备上用 Expo Go，只有当 app 需要 custom native code、store distribution，或 Expo Go 无法运行的能力时，再转向 dev client 或 EAS build。

这样能让 Codex 聚焦 app workflow，而不是第一轮就花在 native IDE setup、simulator setup、provisioning 或 build configuration 上。

#### 使用 Expo plugin

Expo 发布了 [Expo plugin](https://docs.expo.dev/skills/)，为 Codex 提供 Expo-native guidance，覆盖 Expo Router、native UI、forms、navigation、animations、data fetching、NativeWind setup、Expo modules、dev clients、deployment、upgrades 和 Codex Run action wiring。

当 Codex 构建新的 Expo screens、添加 packages、接入 API calls、准备 dev client，或让 app 准备好进入 TestFlight、App Store、Play Store 或 EAS Hosting 时，请使用它。

可选地，当任务需要查询当前 Expo documentation、安装 compatible packages、执行 EAS build 和 workflow operations、screenshots、simulator interaction、React Native DevTools 或 TestFlight data 时，添加 [Expo MCP Server](https://docs.expo.dev/eas/ai/mcp/)。

#### 迭代流程

1. 要求 Codex 检查 repo，并确认这是新的 Expo app 还是现有 Expo project。
2. 从 Expo Router 和 Expo Go 开始；添加 Expo packages 时使用 `npx expo install`。
3. 要求 Codex 构建一个完整 workflow，包含 native-feeling navigation、loading states、empty states 和 error states。
4. 在最快可用路径上验证，例如设备或 simulator 上的 Expo Go；只有在需要时才转向 dev client 或 EAS。

#### 建议后续提示

#### 相关链接

- [Expo plugin](https://docs.expo.dev/skills/)
- [Expo MCP Server setup](https://docs.expo.dev/eas/ai/mcp/)
