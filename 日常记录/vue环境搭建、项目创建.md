环境准备
1、安装node.js
2、安装vue
    vue-cli脚手架初始化Vue3项目
        //	查看@vue/cli版本，确保@vue/cli版本在4.5.0以上
        vue --version
        //	安装或者升级你的@vue/cli
        npm install -g @vue/cli
        //	 创建
        vue create vue_test
        // 启动
        cd vue_test
        npm run serve
    vite初始化Vue3项目
        //	 创建工程
        npm init vite-app <project-name>
        //	进入工程目录
        cd <project-name>
        //	 安装依赖
        npm install
        //	运行
        npm run dev