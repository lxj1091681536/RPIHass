#自动化智能家居系统-RPIHASS  
##Automated Home Automation System - RPIHASS

Abstract
>With the rapid development of modern science and technology and the emergence of a large number of intelligent devices, intelligence has become the pursuit and choice of more and more people. But with the coming of the unified management of intelligent devices. In response to the emergence of intelligent devices on the market, our team designed a Python-based intelligent device terminal control system. This system runs Raspberry system based on Linux on three generations of B + development board of Raspberry Pi. The intelligent systems are all unified and written in Python language and Ymal grammar rules. The intelligent system is compatible with the currently available smart devices based on WiFi and 315 / 433MHz control in the market. The raspberry pie directly accesses the network through a network cable. After the smart hardware device is connected to the WiFi, the system can reversely identify and control the device through the gateway port. At the same time, the device can use the Android mobile phone to construct a real-time monitoring network and monitor and control in real time in the system Make motion recognition camera camera function, the system has excellent human-computer interface, with weather forecast micro-channel function, alarm clock, life advice, convenient for the user's daily life. The system has the advantages of low cost, wide scope of application, remote control function and feasibility, and provides great support for the current development of smart devices.  
>Keywords：Intelligent  devices    Python    remote control     Unified Device Management

目录
>1. 研究意义及目的  
>2. 当前智能硬件终端概述  
>3. 系统总体结构
>>3.1	树莓派系统板  
>>3.2 传感器模块  
>>3.3 显示屏模块  
>>3.4 系统整体结构  
>>3.5系统程序结构  
>>3.6 子模块的调用
>4. 子系统模块介绍  
>5. Python程序功能  
>6. 作品设计优势  
>>6.1 兼容多数智能硬件  
>>6.2 集中管理，远程操作  
>>6.3 界面美观，优化体验  
>>6.4 系统刷新周期短，响应快  
>>6.5 系统休眠功能，低功耗  
>7. 结束语  
>8. 参考文献  

1. 研究意义及目的  
>随着现代科学与技术的高速发展，智能化的设备大量出现，智能化已经成为了越来越多人的追求和选择，但随着而来的是智能化设备的统一管理问题。当前市场中出现的智能化设备大多基于无线控制，家庭中使用一个路由器来作为网络终端即可使用手机或者其他设备远程控制智能设备，不同智能设备公司提供的远程控制终端控制规则往往存在着较大的区别，因此使用者在使用多家公司生产的设备时，需要安装多个控制软件来操控，在一定程度上复杂化了家庭智能设备控制流畅度，不便于消费者操作，因此我们想要开发一套基于Python的智能家居系统来兼容所有智能设备操控程序方案，方便使用者对设备的集中管理。    
>
>用户使用智能硬件设备最大的目标便是在一定程度上方便日常生活，简化流程，帮助人们完成一部分任务，但是当前市场上的硬件设备采用不同的控制方案，用户使用不同的硬件设备需要使用不同的控制终端，在未来随着智能硬件的大量普及，逐渐违背了最初的想法，不仅没有方便人们的生活，反而在控制问题上再一次变得繁琐。各商家之间不做硬件接入交流可以防止被盗用技术，同时也减少了对终端的研究投入。  
但是不做硬件交流的缺点也很明显，效率很低，导致在控制时需要使用大量终端进行控制。智能设备平台可以帮助统一管理智能设备，同时也兼具远程操控功能，具有便利等诸多优点，但是限于开发技术难度和设计厂家之间交流过少，在市场上暂时没有被推广使用。  
我小组的系统采用Python语言编写智能系统，兼具Web端操作界面及安卓、iOS移动App，界面优秀，节省了开发者的研发时间和成本。  

2. 当前智能硬件终端概述  
行业内智能硬件制作厂家众多，国内小米已经建立了巨大的生态链，从基础的网关设备到灯具、路由器等等众多设备都已经构建完成，国外有谷歌等公司开发智能设备。类似两者的其他公司均采用相同的方案来开发，不同的公司开发了不同的控制终端设备，控制方案部分使用WIFI无线控制，WIFI无线控制具有许多有点，在成本低的情况下还能稳定地构建智能系统，减小设备体积，便于携带和控制。  
如果关注小米的可能比较了解，觉得小米智能设备终端是一个智能设备的摇控器，其实它背后不光是一个摇控器，是一个完整的智能家庭、智能硬件服务的平台，摇控器部分只是它的功能子集，包含了所有设备的操控、电商营销众筹平台、场景分享这些。小米智能平台整个APP比较复杂，包括所有智能化接入、众筹孵化、电商对接发货售后。小米平台跟其他电商或者智能平台最大的区别，小米智能是一个完整的闭环。  
小米科技有限责任公司的智能设备生态链在当前行业内处于领先地位，具备趋于完整家具智能设备体系，同时小米也开发了APP--米家智能平台，支持所有小米所有智能设备的接入，但是并不支持其他厂家生产的智能硬件，当前市面上在开发兼容性强的智能终端上还是一个空缺，没有厂家愿意主动长出来为所有智能设备提供接入支持。  

3. 系统总体结构  
RPIHASS系统包括从WEB端控制或传感器接收、树莓派判断到WEB端显示及反馈整个过程。系统主要包括:树莓派系统板、传感器模块、显示屏、手机摄像头监控。树莓派系统板是系统的核心部分,负责监控WEB控制信息、接收传感器信号、监控系统视频数据等反馈信息,并对这些信息进行处理,执行PYTHON程序来处理信息并反馈控制；传感器用来感知和传递外界信息；监控摄像头用来实时监控。   
>>3.1 树莓派系统板  
主板部分我们采用了树莓派三代B+开发板（如图3.1所示）。该主板CPU使用BCM2837  64位的1.2GHZ四核ARM CORTEX-A53，板载1GB内存，自带10/100M自适应网卡支持802.11N WIFI无线网卡，板载低功耗蓝牙4.1 (BLE)， 开发板自带40个GPIO口，可以用来接入传感器或者接入设备。  
我小组编写了大量PYTHON程序，保证整个智能系统在树莓派上实时运行，同时在WEB端显示界面，利用其强大的运算能力，我们接入了传感器和摄像头，传感器采集信息反馈给系统，摄像头采集视频数据发回终端，系统根据传回信息来执行对应PYTHON程序并做出反馈。  
>>3.2 传感器模块  
包括雨滴传感器、温度传感器（树莓派自带）、ESP8266模块、温湿度传感器。  
我把雨滴传感器、温湿度传感器与树莓派GPIO口结合，利用树莓派IO口来读取传感器状态，读取信息来做出不同的系统响应。温度传感器感应树莓派温度，返回温度值执行PYTHON程序，输出PWM来进入三极管控制风扇转速达到无噪音降温的目的。ESP8266模块接入路由局域网，系统通过MTQQ控制ESP8266的GPIO输出状态。  
>>3.3 显示屏模块  
由于系统调试过程中底层PYTHON程序运行状态较为复杂，在调试过程中很容易出现系统无响应、SSH-22端口访问拒绝或者系统WEB平台启动失败，因此使用显示屏来查看树莓派系统运行情况，在出现系统WEB访问失败是通过键盘和显示屏来操控系统重启或者进行回滚操作。在树莓派板上外接一个显示器还可以用来显示WEB端监控视频，这样方便了用户来查看各房间情况。  
显示屏也可以用来显示传感器参数，在调试传感器过程中，常常出现传感器信息反馈错误的问题，用显示器实时显示就能帮助调试找出问题。  
>>3.4 系统整体结构  
系统结构较为简单，有树莓派开发板和显示屏组成，树莓派带外壳，外壳内装有一个树莓派PWM控制的散热风扇，外部为路由器网关，ESP8266作为MTQQ控制器，外接多种传感器。  
>>3.5系统程序结构  
系统整体架构采用PYTHON语法编写，使用APACHE 2.0许可协议，使用PYTHON异步事件驱动系统和ASYNCIO异步框架。在LINUX系统中执行PYTHON来运行整个智能平台系统，同时指定特定文件夹来存放智能系统所运行的所有配置文件。配置文件包括最基础的CONFIGURATION主配置文件、对系统个子模块的描述及描述系统的操控接口的次配置文件。系统根据主配置文件设置系统状态，同时读取次配置文件信息，对系统中的每一个模块做出添加和识别。  
每一个次配置文件均代表着一个子模块，相应的子模块根据次配置文件中的PYTHON程序信息以及配置信息来自启动，接入智能平台系统，需要固定程序控制的子模块会根据配置文件信息来寻找同级程序代码并执行，当所有系统重要子模块均加载正确后，智能系统开始启动，同时开始非系统子模块的加载。  
>>3.6 子模块的调用   
智能系统的使用需要配合大量系统子模块的加载来使用，在CONFIGURATION文件中写入系统模块信息和配置来实现正确调用和配置。在系统启动时我们对非系统子模块采用延时启动的策略，来应对不同模块启动速度不同导致模块间的依赖被打破而导致的系统报错甚至崩溃，这一措施极大地增强了系统的稳定性。 

4. 子系统模块介绍  
>>API：系统能够通过PYTHON程序来调用开源API，并返回程序需要的信息  
>>SENSOR：系统接入各类传感器，传感器采集需要的信息并传回智能系统  
>>SWITCH：使用ESP8266 WIFI模块接入网关，模块的部分GPIO能够使用，使用智能系统来控制IO口实现开关控制或者其他效果  
>>SCRIPTS：系统执行特定脚本来实现对用户动作的响应，同时支持PYTHON_SCRIPTS  
>>GROUPS：该模块为系统子模块，在启动其他子模块后，系统调用组，对WEB端界面或者APP实现分组，美化界面。  
>>DEVICES：在对设备进行反向读取并追踪时，追踪的信息需要保存一段时间提供给系统做出判断，DEVICES组对信息进行分类并做出信息判断识别传给系统识别部分。  
>>TRACKER：系统通过固定端口反向读取硬件设备的状态，并使用WIFI、GPS、ICLOUD账号来实现对设备的追踪。  
>>CUSTOMIZE：该部分由用户编写，能够实现对整个系统的定制，个性化设置智能平台，给用户提供更加良好的体验。  
>>AUTOMATIONS：该部分为系统核心部分，在系统完整启动后开始作用，协调每一个模块之间依赖关系，并判断当前系统和模块状态后做出相应的自动化操作。  

5. Python程序功能  
>>1.	从底层监控树莓派温度，执行PYTHON程序输出PWM变速调节散热风扇，实现无噪音降温  
>>2.	处理SENSOR类传回的数据，对传回数据执行PYTHON程序进行处理和判断，接着传上WEB端显示或者与自动化阈值进行对比执行自动化程序  
>>3.	通过网关特定端口调用手机摄像头及相关控制器，使用PYTHON程序来实现TCP通道的视频流传输，实现在WEB端对摄像头的实时观察和动作检测  
>>4.	使用PYTHON程序来运行NGROK或者DDNS配合端口转发实现对系统的远程控制  
>>5.	执行程序来反向检测网关中接入设备的状态，支持检测IOS设备的电池状态和GPS，支持安卓设备的GPS  

6. 作品设计优势  
>>6.1 兼容多数智能硬件，适用范围广  
我们设计制作的智能平台系统兼容目前市面上大多数的智能硬件，其中包括小米、谷歌等大型生产品牌，对其他小品牌的硬件设备也具有良好的兼容性，同时系统之间接入用户自制硬件设备，支持ESP866、ZIGBEE等WIFI设备。  
>>6.2 集中管理，远程操作  
该智能系统平台将所有的智能硬件设备集中接入，在WEB端或者APP端均可以实时观察状态并进行控制，同时为用户提供统一的接入模式，方便用户自定义接入管理设备，系统具备远程访问功能，用户可以通过移动设备远程管理和控制设备。  
>>6.3 界面美观，优化体验  
我们的智能平台系统具有十分友好的人机交互界面，美观的界面给用户提供良好的使用体验，智能的分组帮助用户更加高效地管理设备。  
>>6.4 系统刷新周期短，响应快  
系统完全使用PYTHON编写，代码执行量小，系统实行30S刷新一次的方案来均衡系统性能和用户体验，部分子模块（天气和网络等）采用30分钟刷新一次来更新数据，在方便用户的同时来减小系统负载。  
>>6.5 系统休眠功能，低功耗  
系统中的摄像头监控具备休眠功能，当监控范围中出现动作达到阈值时，摄像头开启继续监控并拍照。树莓派具备系统休眠功能，对API的调用程序采取25分钟为休眠阈值，超过时间即关闭数据通道，当接收到传入数据时继续开始工作并处理数据。  

7. 结束语  
随着各种高科技产品的发展，智能家居是未来人们生活的必然趋势。智能平台系统能够通过网关端口来逆向识别并控制设备，同时设备可以使用安卓手机构建实时监控网络，在系统中可实时查看监控，并做出动作识别摄像拍照功能，系统具有优秀的人机交互界面，具备天气预报微信功能、闹钟、生活建议，方便了使用者的日常生活。
我们的智能平台系统具有全平台兼容性，在未来智能硬件快速发展的情况下能够适应科技的发展，理论上兼容所有通过无线或者有线方式来控制的智能设备。我们的智能平台系统用户定制度高，用户能够根据个人的喜好来设置系统UI，同时也可以根据用户喜好来定制智能硬件设备并接入系统。该系统构建成本低，适用范围十分广泛，同时具备远程控制功能，。该平台兼具智能硬件的接入，同时也考虑到用户体验，在系统中加入了许多娱乐功能与贴心的生活建议功能，可行性强，为当前智能设备发展提供巨大支持，推广到当前市场完全可行。  

8. 参考文献  
>>① Python官方参考文档（地址https://docs.python.org/3/）

Email <luoxujia1314@gmail.com>
