<template>
  <div class="related-scholar">
    <h2> Related Users </h2>
    <div class="scholar-list">
      <RelatedScholar v-for="scholar in relatedScholars" :userId="scholar"/>
    </div>
  </div>
</template>

<script>
import RelatedScholar from "@/components/UserProfile/RelatedScholar";
export default {
  name: "RelatedScholars",
  components: {RelatedScholar},
  props: ['songId'],
  created() {
    this.$http({
      url: "/api/wholisten",
      params: {
        songid: this.songId
      }
    }).then(res => {
      const data = res.data
      this.relatedScholars = JSON.parse(JSON.stringify(res.data.Users))
    })
  },
  data () {
    return {
      relatedScholars: []
    }
  }
}
</script>

<style lang="less">
@import "../../assets/css/baseStyle";
.related-scholar {
  min-height: 250px;
  h2 {
    display: inline-block;
    font-size: 20px;
    margin: 16px 20px;
    .dot-title(green);
  }
  & > span {
    display: inline-block;
    font-weight: 600;
    font-size: 20px;
    color: @font-medium-grey;
  }
}
.scholar-list {
  display: flex;
  flex-wrap: wrap;
  width: 100%;
  & > div {
    box-sizing: border-box;
    width: 100%;
    display: flex;
    justify-content: flex-start;
    padding: 10px;
    position: relative;
    border-radius: 10px;
    transition: all 0.3s;
    &:hover {
      box-shadow: 0 5px 15px rgba(0,0,0,0.2);
      &:after, &:before {
        position: absolute;
        top: 20%;
        width: 4px;
        content: "";
        background-color: mediumpurple;
        height: 60%;
      }
      &:before{
        left: 0;
      }
      &:after{
        right: 0;
      }
    }
    & > img {
      .avatar-small();
      object-fit: contain;
      border: 3px solid mediumpurple;
    }
    .scholar-info-container {
      margin: 10px 20px;
      color: @font-dark-grey;
      font-weight: 600;
      & > span {
        display: inline-block;
        color: white;
        background-color: mediumpurple;
        font-size: 13px;
        margin-left: 10px;
        padding: 2px 8px;
        border-radius: 4px;
      }
    }
  }
}
</style>