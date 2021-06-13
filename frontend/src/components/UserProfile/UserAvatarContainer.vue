<template>
  <div class="user-avatar-container">
    <div class="user-avatar-wrap">
      <img :src="imgurl" alt="">
      <div class="user-basic-info">
        <h2> {{name}} </h2>
        <span><i class="fa fa-angle-double-up"/> LV. {{level}} </span>
        <span><i class="fa fa-location-arrow"/> Shanghai, China Mainland </span>
        <span><i class="fa fa-quote-left"/> {{signature}} </span>
      </div>
    </div>
    <i class="follow-button fa fa-ellipsis-v"/>
    <div class="user-stat">
      <div>
        {{citeCount}}
        <span> Songs </span>
      </div>
      <div>
        {{ paperCount }}
        <span> Follow </span>
      </div>
      <div>
        {{hIndex}}
        <span> Follower </span>
      </div>
    </div>
  </div>
</template>

<script>
function nameToUpperCase (str) {
  return str.toLowerCase().replace(/( |^)[a-z]/g, (L) => L.toUpperCase());
}
export default {
  name: "UserAvatarContainer",
  props: ['userId'],
  created() {
    this.$http({
      url: "/api/userinfo",
      params: {
        userid: this.userId,
      }
    }).then(res => {
      const data = res.data
      this.name = data.username
      this.imgurl = data.avatarurl
      this.level = data.level
      this.citeCount = data.songcount
      this.paperCount = data.follows
      this.hIndex = data.follower
      this.signature = data.signature
    }).catch(e => {})

  },
  data () {
    return {
      name: "",
      imgurl: "",
      level: 0,
      citeCount: 0,
      paperCount: 0,
      hIndex: 0,
      signature: ""
    }
  }
}
</script>

<style lang="less">
@import "../../assets/css/baseStyle";
.user-avatar-container {
  position: relative;
  .display-card();
  padding: 10px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  .user-avatar-wrap {
    width: 100%;
    position: relative;
    display: flex;
    justify-content: flex-start;
    img {
      margin: 20px;
      width: 80px;
      height: 80px;
      border-radius: 50%;
      object-fit: contain;
      border: 2px solid mediumpurple;
    }
    .user-basic-info {
      display: flex;
      flex-direction: column;
      h2 {
        font-size: 20px;
        margin-bottom: 10px;
      }
      span {
        display: block;
        font-size: 14px;
        font-weight: 600;
        color: #979797;
        margin: 3px 0;
        i {
          margin-right: 10px;
          color: mediumpurple;
        }
      }
    }
  }
}
.user-stat {
  width: 70%;
  margin: 10px;
  display: flex;
  justify-content: space-between;
  & > div {
    text-align: center;
    font-weight: 600;
    font-size: 22px;
    & > span {
      display: block;
      font-size: 12px;
      color: @font-medium-grey;
      font-weight: 400;
    }
  }
}
.follow-button {
  position: absolute;
  transition: all 0.3s;
  right: 40px;
  top: 20px;
  &:hover {
    color: mediumpurple;
  }
}
</style>