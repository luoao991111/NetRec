<template>
  <div class="profile-wrapper">
    <div class="profile-top-container">
      <div class="profile-left-box">
        <UserAvatarContainer :userId="userId" :key="'avatar-container' + userId"/>
      </div>
      <div class="profile-right-box">
        <CitedPaper :relatedPapers="paperList" :genre="'cited'"></CitedPaper>
      </div>
    </div>
  </div>
</template>

<script>
import RelatedScholars from "@/components/UserProfile/RelatedScholars";
import UserAvatarContainer from "@/components/UserProfile/UserAvatarContainer";
import renderLineChart from "@/utils/ECharts-LineChart";
export default {
  name: "UserProfile",
  beforeRouteUpdate (to, from, next) {
    next()
    if (to.path.startsWith('/profile') && from.params.id !== to.params.id) {
      this.renderData()
    }
  },
  created() {
    this.userId = this.$route.params.id
    this.renderData()
  },
  mounted() {
    // this.renderSvg()
  },
  components: {
    UserAvatarContainer,
    HistoryChart: () => import("@/components/UserProfile/HistoryChart"),
    RelatedScholars,
    CitedPaper: () => import("@/components/Paper/CitedPaper")
  },
  data () {
    return {
      following: false,
      tags: [],
      userId: 0,
      name: "",
      citationTrend: [],
      cited: 0,
      eduList: {},
      workList: {},
      paperList: []
    }
  },
  methods: {
    renderData () {
      this.userId = this.$route.params.id
      this.$http({
        url: "/api/record",
        params: {
          userid: this.userId
        }
      }).then(res => {
       this.paperList = res.data.record.map(d => d.songid)
      })
    },
    renderSvg () {
      this.$http({
        url: "/api/ptrend",
        params: {
          local_id: this.userId
        }
      }).then(res => {
        let i = 0
        for (const item of res.data.trend) {
          this.$set(this.citationTrend, i, {time: item.year, value: item.citation_count})
          i++
        }
        return new Promise(resolve => resolve())
      }).then(res => {
        const svg = this.$refs["cited-trend"]
        // const chart = new LineChart({
        //   target: svg,
        //   width: 320,
        //   height: 200,
        //   xTicks: 3,
        //   yTicks: 3
        // })
        const svgData = JSON.parse(JSON.stringify(this.citationTrend))
        // chart.render(svgData)
        renderLineChart(svg, svgData)
      })
    }
  }
}
</script>

<style scoped lang="less">
@import "../assets/css/baseStyle";
@import "../assets/css/lineChart.css";
.profile-wrapper {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 100%;
  flex-direction: column;
}
.profile-top-container {
  width: 80%;
  display: flex;
  justify-content: flex-start;
  .profile-left-box {
    width: 40%;
    box-sizing: border-box;
    display: flex;
    flex-direction: column;
    justify-content: flex-start;
    & > div {
      .display-card();
      padding: 10px;
      h2 {
        .dot-title(purple);
      }
    }
  }
  .profile-right-box {
    width: 60%;
    & > div {
      .display-card();
      padding: 10px;
    }
  }
}
.follow-button {
  .button-base();
  position: absolute;
  bottom: 10px;
  right: 10px;
}
.tag-list {
  list-style: none;
  padding: 0;
  margin: 0;
  display: flex;
  justify-content: flex-start;
  flex-wrap: wrap;
  & > li {
    padding: 2px 5px;
    margin: 0 4px;
    background-color: #e7e7e7;
    border-radius: 5px;
    font-size: 12px;
    &.add-tag {
      background-color: transparent;
      color: @font-dark-grey;
      cursor: pointer;
    }
  }
}
.history-container {
  position: relative;
  &>h2 {
    display: inline-block;
    font-size: 20px;
    margin: 16px 20px;
    .dot-title(orange);
  }
}
</style>