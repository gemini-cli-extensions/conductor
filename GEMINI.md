# Conductor Context

If a user mentions a "plan" or asks about the plan, and they have used the conductor extension in the current session, they are likely referring to the `conductor/tracks.md` file or one of the track plans (`conductor/tracks/<track_id>/plan.md`).

## Universal File Resolution Protocol

**PROTOCOL: How to locate files.**
To find a file (e.g., "**Product Definition**") within a specific context (Project Root or a specific Track):

1.  **Identify Index:** Determine the relevant index file:
    -   **Project Context:** `conductor/index.md`
    -   **Track Context:**
        a. Resolve and read the **Tracks Registry** (via Project Context).
        b. Find the entry for the specific `<track_id>`.
        c. Follow the link provided in the registry to locate the track's folder. The index file is `<track_folder>/index.md`.
        d. **Fallback:** If the track is not yet registered (e.g., during creation) or the link is broken:
            1. Resolve the **Tracks Directory** (via Project Context).
            2. The index file is `<Tracks Directory>/<track_id>/index.md`.

2.  **Check Index:** Read the index file and look for a link with a matching or semantically similar label.

3.  **Resolve Path:** If a link is found, resolve its path **relative to the directory containing the `index.md` file**.
    -   *Example:* If `conductor/index.md` links to `./workflow.md`, the full path is `conductor/workflow.md`.

4.  **Fallback:** If the index file is missing or the link is absent, use the **Default Path** keys below.

5.  **Verify:** You MUST verify the resolved file actually exists on the disk.

**Standard Default Paths (Project):**
- **Product Definition**: `conductor/product.md`
- **Tech Stack**: `conductor/tech-stack.md`
- **Workflow**: `conductor/workflow.md`
- **Product Guidelines**: `conductor/product-guidelines.md`
- **Tracks Registry**: `conductor/tracks.md`
- **Tracks Directory**: `conductor/tracks/`

**Standard Default Paths (Track):**
- **Specification**: `conductor/tracks/<track_id>/spec.md`
- **Implementation Plan**: `conductor/tracks/<track_id>/plan.md`
- **Metadata**: `conductor/tracks/<track_id>/metadata.json`
- **Verification Images**: `conductor/tracks/<track_id>/images/` (按需动态创建)

## Conductor Spec-First & SDD/TDD Safeguard (规范驱动开发铁律)

- **规范先行，绝不盲目改码（Spec-First Before Code Modification）**：
  在任何引入或存在 Conductor 体系（工作区含有 `conductor/` 目录或用户提及相关流程）的工程中，**严禁绕过 Conductor 流程直接对物理源码进行修改写入（Write/Replace）**。开发与修改必须严格遵循“先规范（SDD）、后计划（TDD）、再编码（Implementation）”的三阶递进流程：
  1. **建轨与备案先行**：任何功能迭代、临时调试开关或缺陷修复，必须首先在相关仓库的 `conductor/` 下创建或选定独立轨道（Track）。
  2. **双文档对齐门禁与写码前置断言（SDD/TDD Pre-Flight Assertion）**：
     - **写码前置物理断言**：在调用 `replace`、`write_file` 对生产源码或**测试用例**执行任何物理修改前，必须在思考域 `<thought>` 中执行物理断言：`ASSERT(本次修改是否已在 plan.md 中立项且 spec.md 已定义？)`。未立项严禁动码！
     - **微小改动零豁免（Zero Exemption for Triviality）**：无论改动是一行测试代码、一个超时常量、一个日志打印还是配置文件，严禁心存侥幸将其视作“琐碎修改”而跳过文档更新。在规范驱动开发中，任何未在 spec/plan 中记录的代码改动一律视作非法入侵（Illegal Mutation）。
     - **交互顺序状态机锁定**：在代码审查（Review）或方案推演阶段，一旦收到用户“认可方案/同意修复/开始执行”指令，状态机的第一动作强制锁定为：先更新 `spec.md` 与 `plan.md`，第二动作才允许执行代码修改。
  3. **母语化表达规约**：在编写 Conductor 相关文档（`spec.md`、`plan.md`、`index.md` 等）时，严格遵循**“技术术语保留原生英文，正文使用流畅规范的简体中文”**，杜绝纯英文输出，贴合母语沉浸式审阅体验。
  4. **隐式防泄与工作区隔离**：Conductor 的轨道元数据与工作流文件必须严格登记在本地 Git 的 `.git/info/exclude` 中，严禁污染公共 `.gitignore` 或误提入代码仓库。
  5. **生产环境防呆防线**：对于仅用于现场排障或临时调试的代码变更（如高频日志、打桩插桩），严禁直接物理删除原有逻辑，必须使用 `#if 0 ... #endif` 预编译指令包裹并标注醒目的 `TODO(Debug)` 注释，确保排障后一键还原，誓死防范高负载调试代码误合入生产分支。
  6. **GUI 桌面端视觉验证与动态对账防线（GUI Screenshot Verification & Lazy Directory Creation）**：对于涉及图形界面、Qt/QML 或桌面端视觉渲染的任务，验收必须包含物理截图对账。在执行阶段按需动态创建 `conductor/tracks/<track_id>/images/` 目录；捕获渲染截图存入该目录并关联至 `plan.md` 或验证报告中，若存在截图则同步在 `index.md` 中挂载 `- [Verification Images](./images/)` 索引；对于无界面的纯后端/底层服务任务，严禁预先创建空 `images/` 目录，以捍卫工作区纯净。

