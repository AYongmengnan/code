<template>
  <div class="vuevideo">
    <video controls>
      <source :src="video_url" type="video/mp4">
      <source :src="video_url" type="video/avi">
      <source :src="video_url" type="video/mkv">
      <source :src="video_url" type="video/mov">
    </video>
  </div>
</template>

<script lang="ts" setup name="VideoPlayer">
  let video_url = 'http://imdiona.com:8052/files/01b307acba4f54f55aafc33bb06bbbf6ca803e9a/1234567890_1712748330031.mp4'
  

</script>