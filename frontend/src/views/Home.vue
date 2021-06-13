<template>
  <div class="home">
    <Carousel/>
    <div class="clearfix">
      <div class="sidebar-content">
        <div class="featured-items">
        </div>
      </div>
      <div class="main-content">
        <nav class="tab-menu" :style="{'--tag-position': translateTag}">
          <router-link v-for="(link, index) in links"
                       :to="link.to"
                       tag="span" active-class="active">
            {{link.desc}}
          </router-link>
        </nav>
        <keep-alive>
          <router-view/>
        </keep-alive>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
export default {
  name: 'Home',
  created() {
  },
  components: {
    AuthorInfo: () => import("@/components/Home/AuthorInfo"),
    Carousel: () =>  import("@/components/Home/Carousel"),
    PaperInfo: () => import("@/components/Home/PaperInfo")
  },
  data () {
    return {
      recAuthors: [],
      links: [
        {
          to: "/home/index",
          desc: "All Genres"
        }
      ],
    }
  },
  computed: {
    tagPosition () {
      let currentRoute = this.$route.path
      return this.links.findIndex(link => link.to === currentRoute)
    },
    translateTag () {
      return -140 * (this.links.length - this.tagPosition - 1) + "px"
    }
  }
}
</script>
<style scoped>
.sidebar-content {
  width: 20%;
  float: left;
  padding: 40px;
  box-sizing: border-box;
}
.sidebar-content h2 {
  font-size: 22px;
  color: #767676;
  font-weight: 500;
  margin-left: 10px;
}
.main-content {
  width: 80%;
  float: left;
  box-sizing: border-box;
  margin-top: 100px;
}
.featured-items {
  min-height: 600px;
}
.tab-menu {
  position: relative;
  display: flex;
  width: 100%;
  justify-content: flex-start;
  float: right;
  padding: 10px 40px 20px 40px;
  border-bottom: 1px solid #e7e7e7;
  box-sizing: border-box;
}
.tab-menu > span {
  min-width: 140px;
  font-weight: 600;
  cursor: pointer;
  text-align: center;
  color: #767676;
}
.tab-menu > span.active {
  font-weight: 800;
  color: #565656;
}
.tab-menu:after {
  content: "";
  height: 4px;
  width: 60px;
  background-color: mediumpurple;
  position: absolute;
  bottom: 0;
  left: 80px;
  transition: all 0.3s ease-in-out;
  box-shadow: 0 -5px 20px mediumpurple;
  transform: translateX(var(--tag-position));
}
</style>
