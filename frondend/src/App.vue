<script setup>
import { useRoute } from 'vue-router';
import { onMounted } from 'vue';

const route = useRoute();
onMounted(()=>{
    document.title = "Just-Test"
})
</script>

<template>
  <el-container class="full-container">
    <el-header>Just-Test</el-header>
    <el-container>
      <el-aside width="15%"><el-menu
        default-active="1"
        class="el-menu-vertical-demo"
        @open="handleOpen"
        @close="handleClose"
      >
        <el-menu-item index="1">
          <el-icon><icon-menu /></el-icon>
          <span>文件</span>
        </el-menu-item>
        <el-menu-item index="2">
          <el-icon><document /></el-icon>
          <span>脚本监控</span>
        </el-menu-item>
        <el-menu-item index="3">
          <el-icon><setting /></el-icon>
          <span>学习资料</span>
        </el-menu-item>
      </el-menu></el-aside>
      <el-main><router-view></router-view></el-main>
    </el-container>
  </el-container>
</template>

<style>
/* 全局重置，建议放在单独的 CSS 文件中 */
html, body {
  margin: 0;
  padding: 0;
  height: 100%;
}

/* 让整个容器充满视口高度 */
.full-container {
  height: 100vh;
}

.el-header {
  background-color: #B3C0D1;
  color: #333;
  text-align: center;
  line-height: 60px;
}

.el-aside {
  background-color: #D3DCE6;
  color: #333;
  text-align: center;
  line-height: 200px;
}

.el-main {
  background-color: #E9EEF3;
  color: #333;
  text-align: center;
  line-height: 160px;
}
</style>