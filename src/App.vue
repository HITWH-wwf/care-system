<template>
  <div id="app">
    <transition name="el-zoom-in-top">
      <router-view></router-view>
    </transition>
  </div>
</template>

<script>
export default {
  name: 'app',
  components: {
  }
}
</script>

<style>
html,body{
  margin: 0;
  padding: 0;
}
#app {
  position: absolute;
  top: 0px;
  bottom: 0px;
  width: 100%;
}
</style>
