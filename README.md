## 用法

首先编辑 `main.py` 中的 `COURSES` 变量，内容为 `(课程号, 编号)` 元组的列表。

然后执行：

```
python main.py --login --phase=1
```

- `--login` 表示手动登陆并保存 cookies 到 `cookies.json`

    > 无 `--login` 则使用 `cookies.json` 中的 cookies

- `--phase` 指定选课阶段

    `1` 为必修课、专业选修课

    `2` 位任选课、其他专业课程

此外可以使用 `python main.py --ring` 来事先测试响铃（响铃目前只兼容 Mac，其他系统自己改下，暂时没空改）。