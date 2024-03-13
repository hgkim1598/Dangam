<template>
  <div>
    <b-navbar type="dark" class="my-navbar" variant="">
      <b-navbar-brand href="/four" class="logo-container"><img src="@/assets/llogo.png" alt="로고 이미지"></b-navbar-brand>
      <b-navbar-toggle target="nav_collapse"/>
      <b-collapse is-nav id="nav_collapse">
        <b-navbar-nav pills>
          <b-nav-item href="/four" :class="{'active': $route.path === '/four'}" @click="handleItemClick('/four')" link-classes="custom-text-color">사자성어</b-nav-item>
          <b-nav-item href="/wise" :class="{'active': $route.path === '/wise'}" @click="handleItemClick('/wise')" link-classes="custom-text-color">명언</b-nav-item>
          <b-nav-item href="/ImageCrawling" :class="{'active': $route.path === '/ImageCrawling'}" @click="handleItemClick('/ImageCrawling')" link-classes="custom-text-color">이미지 크롤링</b-nav-item>
          <b-nav-item href="/imggen" :class="{'active': $route.path === '/imggen'}" @click="handleItemClick('/imggen')" link-classes="custom-text-color">이미지생성</b-nav-item>
        </b-navbar-nav>
      </b-collapse>
    </b-navbar>
  </div>
</template>

  
  <script>
  export default {
    name: "Header",
    methods: {
      handleItemClick(route) {
        this.$router.push(route);
      }
    }
  }

</script>

<style>
.my-navbar {
  background-color: #f0ce9b; 
  color: black; 
}
.logo-container img {
  max-width: 100px;
  max-height: 100px;
  margin-left: 40px;
}

.custom-text-color {
  font-size: 20px !important;
  color: black !important;
  font-weight: bold !important;
  margin-right: 20px;
  margin-left: 20px;
}

.active .custom-text-color {
  color: #EB4C10 !important;
}

</style>
