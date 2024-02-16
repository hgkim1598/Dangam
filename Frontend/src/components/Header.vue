<template>
    <div>
        <b-navbar toggleable="lg" type="dark" variant="info">
            <b-navbar-brand href="#">Dangam🧧</b-navbar-brand>
            <b-navbar-toggle target="nav_collapse"/>
            <b-collabse is-nave id="nav_collase">
                <b-navbar-nav>
                    <b-nav-item to="/">사자성어</b-nav-item>
                    
                    <b-nav-item href="#">명언</b-nav-item>
                </b-navbar-nav>
            </b-collabse>
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