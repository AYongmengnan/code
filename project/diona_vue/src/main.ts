// 引入createApp用于创建应用
import { createApp } from "vue";
// 引入App根组件

import App from './App.vue'


// createApp(App).mount('#app')

let app = createApp(App)

import VueVideoPlayer from '@videojs-player/vue'
import 'vue3-video-play/dist/style.css' // 引入css
app.use(VueVideoPlayer)

app.mount('#app')