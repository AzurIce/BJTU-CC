# BJTU-CC

BJTU 的选课脚本

流程：

- 脚本自动查找目标课程勾选并点击提交，然后响铃提醒

- 人工输入验证码并提交。
- 输入 y/n 来退出

## 依赖

Python3（我用的 3.11）

MacOS/Linux:

```
pip install selenium
```

Windows:

```
pip install selenium winsound
```

## 用法

首先编辑 `main.py` 中的 `COURSES` 变量，内容为 `(课程号, 编号)` 元组的列表。

然后执行：

```
python main.py --login --phase 1
```

- `--login` 表示手动登陆并保存 cookies 到 `cookies.json`

    > 无 `--login` 则使用 `cookies.json` 中的 cookies

- `--phase` 指定选课阶段

    `1` 为必修课、专业选修课

    `2` 位任选课、其他专业课程

此外可以使用 `python main.py --ring` 来事先测试响铃。