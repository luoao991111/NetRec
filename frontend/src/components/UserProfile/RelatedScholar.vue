<template>
  <div @click="jumpToUser">
    <img :src="imgurl" alt="">
    <div class="scholar-info-container">
      {{name}}
      <span> lv {{level}} </span>
    </div>
  </div>
</template>

<script>
function nameToUpperCase (str) {
  return str.toLowerCase().replace(/( |^)[a-z]/g, (L) => L.toUpperCase());
}
export default {
  name: "RelatedScholar",
  props: ['userId'],
  created() {
    this.$http({
      url: "/api/userinfo",
      params: {
        userid: this.userId
      }
    }).then(res => {
      const data = res.data
      this.name = data.username
      // this.name = this.name.join(" ")
      // this.name = nameToUpperCase(this.name)
      this.imgurl = data.avatarurl
      this.level = data.level
      // this.affiliation = data.affiliation
    })
  },
  data () {
    return {
      name: "",
      level: "",
      imgurl: ""
    }
  },
  methods: {
    jumpToUser () {
      this.$router.push('/profile/' + this.userId)
    }
  }
}
</script>

<style scoped>
</style>