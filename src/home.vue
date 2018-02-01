<template>
    <div style="width:100%">
        <headerCompone>
        </headerCompone>
        <div class="content">
            <transition name="el-fade-in">
                <router-view></router-view>
            </transition>
        </div>
    </div>
</template>

<script>

import headerCompone from '@/components/header/header.vue'

export default {
    data() {
        return {
        }
    },
    components: {
        headerCompone
    }
}
</script>

<style scoped>
.content {
    top: 60px;
}
</style>

