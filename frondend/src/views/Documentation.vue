<template>
    <div class="card-container" style="display: flex;">
      <el-card shadow="hover" style="max-width: 300px;">
        <template #header>
          <div>
            <a href="https://pytest.cn/en/stable/getting-started.html">Pytest</a>
          </div>
        </template>
        <div class="card-content">          
            <el-text type="info" size="large">
                pytest 框架使编写简短、易读的测试变得简单，并且可以扩展以支持应用程序和库的复杂功能测试。
            </el-text>
        </div>
      </el-card>
      <el-card shadow="hover" style="max-width: 300px;margin-left: 3%;">
        <template #header>
          <div class="card-header">
            <a href="https://robotframework.org/">RobotFramework</a>
          </div>
        </template>
        <div class="card-content">
            <el-text type="info" size="large">
                机器人框架是一个用于测试自动化和机器人流程自动化 （RPA） 的开源自动化框架。它得到了机器人框架基金会的支持，并在行业中得到广泛应用 。
                其人性化且通用的语法使用关键字并支持通过库进行扩展 Python、Java 和其他语言。
                它与其他工具集成，无需许可费即可实现全面自动化，并由拥有数百个第三方库的丰富社区提供支持。
            </el-text>
        </div>
      </el-card>
      <el-card shadow="hover" style="max-width: 300px;margin-left: 3%;">
        <template #header>
          <div class="card-header">
            <a href="https://allurereport.org/docs/pytest/">Allure Pytest</a>
          </div>
        </template>
        <div class="card-content">
            <el-text type="info" size="large">
                使用 Allure Report 和 pytest 测试生成漂亮的 HTML 报告。
            </el-text>
        </div>
      </el-card>
    </div>
  </template>
  
  <script lang="ts" setup>
  </script>
  
  <style scoped>
  /* 调整 header 高度 */
  .card-container :deep(.el-card__header) {
    padding: 6px 16px;
    line-height: 1;
    margin: 0; /* 清除默认外边距 */
  }
  
  /* 调整 footer 高度 */
  .card-container :deep(.el-card__footer) {
    padding: 6px 16px;
    line-height: 1;
    margin: 0;
  }
  
  /* 核心：调整内容区的内边距和标签默认样式 */
  .card-container :deep(.el-card__body) {
    padding: 6px 16px; /* 内容区默认上下内边距是 20px，大幅减小 */
    line-height: 1;
  }
  
  /* 清除 <p> 标签的默认外边距和行高 */
  .card-content p {
    margin: 0; /* 清除 p 标签默认的上下外边距 */
    line-height: 1; /* 行高和文字大小一致，避免空白 */
    font-size: 14px; /* 可选：统一文字大小 */
  }
  </style>