# 山西职业技术学院辅助软件

欢迎来到山西职业技术学院！本项目致力于为同学们提供便捷的辅助功能，让你能够省去繁琐的功能，节省宝贵的时间，提升个人效率。通过这个项目，你可以利用现代技术手段，实现辅助功能。

无论你是想学习还是如何利用编程辅助自己解决实际问题，还是简单地希望减少每天的重复操作，这个项目都能为你提供一个很好的学习和实践机会。希望你能享受带来的便利，并在此基础上探索更多有趣的应用！

## 功能介绍

- **自动打卡**：自动完成每日打卡
- **成绩推送**：通过微信通知用户成绩

## 使用方法
  1.你首先需要**Fork**这个项目<br>
  2.点击并关注<a href="https://push.showdoc.com.cn/">**showdoc推送服务</a>获取你的API**<br>
  3.前往你Fork项目中的**Settings**中的**Secrets and variables**中的**Actions**，并点击**New repository secret**<br>
  4.添加以下内容
  - （1）添加ID_NO，内容为你的身份证号码
  - （2）添加SCHOOL_ADDRESS，内容为学校地址<br>
  参考学校地址：<br>
    中国山西省太原市迎泽区龙堡街_山西职业技术学院(长风校区)<br>
    中国山西省晋中市榆次区兴业街_山西职业技术学院(南校区)<br>
    中国山西省太原市小店区_山西职业技术学院(南中环校区)<br>
  - （3）添加HOLIDAY_ADDRESS，内容为放假地址<br>
  参考地址：<br>
    X国XX省XX市XX县(区)_XX小区<br>
  - （4）添加STUDENT_ID，内容为你的学号
  - （5）添加PASSWORD，内容是你教务系统的登录密码（务必填写正确）
  - （6）填写PUSH_MESSAGE_TOKEN，内容是你的完整的专属推送地址

  5.在Switch中开启/关闭：填写开启或关闭，用来控制运行是否启动
    

## 特别感谢
  ### 特别感谢：<a href="https://github.com/deijing">初沐</a>提供的技术支持，同时也感谢GitHub、Python、requests库、ddddocr库、rsa库、Regable软件、Charles软件、JetBrains提供的软件与技术支持
  ### 项目源代码
  **<a href="https://github.com/wangzhenxing4/AutoDailyAttendance">山西职业技术学院自动每日打卡任务</a>** 的自动完成打卡源代码
  <br>
  **<a href="https://github.com/wangzhenxing4/ScoreUpdateReminder">山西职业技术学院成绩更新自动推送</a>** 的获取成绩更新源代码
## 其他问题
  - 如果在使用过程中遇到任何问题或有其他建议，欢迎随时联系我们，我们将竭诚为你提供支持和帮助。祝愿你在山西职业技术学院的学习生活中一切顺利！
## 版权许可
  - 当前项目受到Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International版权保护
<p xmlns:cc="http://creativecommons.org/ns#" xmlns:dct="http://purl.org/dc/terms/"><a property="dct:title" rel="cc:attributionURL" href="https://github.com/wangzhenxing4/Auxiliary-software-of-shanxi-polytechnic-college">Auxiliary software of shanxi polytechnic college</a> by <a rel="cc:attributionURL dct:creator" property="cc:attributionName" href="http://wangzhenxing4.github.io">王振兴</a> and <a rel="cc:attributionURL dct:creator" property="cc:attributionName" href="https://github.com/deijing">初沐</a> is licensed under <a href="https://creativecommons.org/licenses/by-nc-sa/4.0/?ref=chooser-v1" target="_blank" rel="license noopener noreferrer" style="display:inline-block;">Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International<img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/cc.svg?ref=chooser-v1" alt=""><img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/by.svg?ref=chooser-v1" alt=""><img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/nc.svg?ref=chooser-v1" alt=""><img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/sa.svg?ref=chooser-v1" alt=""></a></p>
