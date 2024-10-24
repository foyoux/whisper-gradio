# whisper-gradio
从 音频、视频 中生成字幕，并翻译

[whisper](https://github.com/openai/whisper) 支持多种模型，代码中没有全部加载，防止占用过多资源，可以根据自己的需求在代码中加载（在 `MODELS` 处注释或取消注释）。

[pygtrans](https://github.com/foyoux/pygtrans) 用于字幕翻译，默认需要科学上网，如果没有全局梯子，可以在代码中自行设置代理。设置方法具体参见 `pygtrans` 项目。 


## 效果展示

> 示例视频来自：
>
> https://dr-stone.jp/
>
> https://www.youtube.com/watch?v=xdF_d7aqu1Q&ab_channel=TOHOanimation%E3%83%81%E3%83%A3%E3%83%B3%E3%83%8D%E3%83%AB

<details><summary>点击展开</summary>
<p>

![image](https://github.com/user-attachments/assets/736ae0a9-9616-4626-afdc-fcda4ba98317)

![image](https://github.com/user-attachments/assets/faffa95c-a7b3-4f5f-9ed7-c74f6a6f40a6)

![image](https://github.com/user-attachments/assets/4ec1e05f-84b4-4791-8ada-9b3d5b04da17)

</p>
</details>
