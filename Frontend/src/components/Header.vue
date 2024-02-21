<template>
    <div>
        <b-navbar type="dark" class="my-navbar">
            <b-navbar-brand href="/four">Dangam🧧</b-navbar-brand>
            <b-navbar-toggle target="nav_collapse"/>
            <b-collapse is-nav id="nav_collapse">
                <b-navbar-nav>
                    <b-nav-item to="/four">사자성어</b-nav-item>
                    
                    <b-nav-item href="/wise">명언</b-nav-item>
                </b-navbar-nav>
            </b-collapse>
        </b-navbar>
    </div>
</template>

<script>
export default {
    name: "Header",
    data() {
        return {};
    }
}
</script>

<style>
.my-navbar {
    background-color: #EB4C10; /* 이 색상에 대한 CSS 클래스를 정의합니다. */
}
</style>