<template>
  <div class="music-wrapper">
    <div>
      <div class="music-player">
        <div class="left-box">
          <img :src="coverUrl" alt=""
               class="music-cover" :class="{'spinning': playing}">
          <audio :src="musicSrc" ref="audio" @timeupdate="updateTime"/>
          <div class="music-progress-full" @click="setAudioTime" ref="progress-bar">
            <div class="music-progress" :style="'--scale:' + progress * 100 + '%'">
            </div>
          </div>
          <div class="music-control">
            <div class="control-item"> <i class="fa fa-step-backward"></i> </div>
            <div class="control-item center" @click="playMusic">
              <i class="fa fa-play" v-if="!playing"></i>
              <i class="fa fa-pause" v-else></i>
            </div>
            <div class="control-item"> <i class="fa fa-step-forward"></i> </div>
          </div>
        </div>
        <div class="right-box">
          <h2> {{name}} </h2>
          <span class="basic-info"> <i class="fa fa-user-circle-o"/> {{artist}} </span>
          <span class="basic-info"> <i class="fa fa-bookmark-o"/> {{album}} </span>
          <section class="lyrics-container" v-if="lyrics.length > 0">
            <i v-for="(lyric, index) in lyrics"
            :class="{'active': lyricIndex === index + 1}"
            :style="'transform: translateY(-' + lyricOffset * 97.5 + '%)'">
              {{lyric.text}}
            </i>
          </section>
          <section class="lyrics-container" v-else>
            <i class="pure-music"> 纯音乐，敬请欣赏 </i>
          </section>
        </div>
      </div>
      <div class="music-rec">
        <div class="music-recommend">
          <h2> Recommened Works </h2>
          <CitedPaper :genre="'cited'" :related-papers="relatedWorks" :key="id"/>
        </div>
        <RelatedScholars :song-id="id" :key="id"/>
      </div>
    </div>
  </div>
</template>

<script>
import CitedPaper from "../components/Paper/CitedPaper";
import RelatedScholars from "../components/UserProfile/RelatedScholars";
export default {
  name: "Music",
  components: {RelatedScholars, CitedPaper},
  beforeRouteUpdate (to, from, next) {
    next()
    this.renderData()
  },
  created() {
    this.renderData()
  },
  data () {
    return {
      playing: false,
      musicSrc: "",
      lyrics: [],
      coverUrl: "",
      lyricIndex: 0,
      id: 0,
      name: "",
      artist: "",
      album: "",
      relatedWorks: [],
      progress: 0
    }
  },
  methods: {
    playMusic () {
      const audio = this.$refs['audio']
      if (this.playing)
        audio.pause()
      else audio.play()
      this.playing = !this.playing
    },
    updateTime (e) {
      const currentTime = e.target.currentTime
      this.progress = currentTime / e.target.duration
      while (currentTime > this.lyrics[this.lyricIndex].time)
        this.lyricIndex ++
    },
    renderData () {
      console.log('rendered')
      this.playing = false
      this.id = this.$route.params.id
      this.progress = 0
      this.lyricIndex = 0
      this.$http({
        url: "/api/lyric",
        params: {
          songid: this.id
        }
      }).then(res => {
        this.lyrics = []
        let timeStamp, text
        for (const lyric of res.data.lyrics) {
          timeStamp = lyric.match(/(?<=\[).*?(?=])/)[0]
          timeStamp = parseInt(timeStamp.match(/.*(?=:)/)[0]) * 60 + parseFloat(timeStamp.match(/(?<=:).*/))
          text = lyric.match(/(?<=]).*/)[0]
          this.lyrics.push({time: timeStamp, text})
        }
      })
      this.$http({
        url: "/song/url",
        params: {
          id: this.id
        }
      }).then(res => {
        this.musicSrc = res.data.data[0].url
      })
      this.$http({
        url: "/api/songinfo",
        params: {
          songid: this.id
        }
      }).then(res => {
        this.name = res.data.name
        this.coverUrl = res.data.coverurl
        this.artist = res.data.singer[0]
        this.album = res.data.collection
      })

      this.$http({
        url: '/api/pagerec',
        params: {
          songid: this.id
        }
      }).then(res => {
        this.relatedWorks = res.data.Recomend
      })
    },
    setAudioTime (e) {
      const audio = this.$refs["audio"]
      const x = e.offsetX / this.$refs["progress-bar"].offsetWidth
      const duration = audio.duration
      audio.currentTime = x * duration
      const currentTime = audio.currentTime
      this.lyricIndex = 0
      this.progress = x
      while (currentTime > this.lyrics[this.lyricIndex].time)
        this.lyricIndex ++
    }
  },
  computed: {
    lyricOffset () {
      if (this.lyricIndex <=5) return 0
      else return this.lyricIndex - 5
    }
  }
}
</script>

<style lang="less">
@import "../assets/css/baseStyle";

.music-wrapper {
  width: 100%;
  display: flex;
  justify-content: center;
  flex-direction: column;
  align-items: center;
  & > div {
    width: 80%;
    padding: 10px;
    display: flex;
    flex-direction: column;
    .music-recommend {
      width: 60%;
      .display-card();
      padding: 20px;
    }
    .music-rec {
      display: flex;
      justify-content: flex-start;
      .related-scholar {
        .display-card();
        width: 40%;
        padding: 10px;
      }
    }
    .music-player {
      display: flex;
      justify-content: flex-start;
      .display-card();
      padding: 40px;
    }
  }
}
.music-player {
  .left-box {
    display: flex;
    justify-content: center;
    align-items: center;
    flex-direction: column;
    width: 50%;
    img.music-cover {
      height: 300px;
      width: 300px;
      border-radius: 50%;
      box-shadow: 0 5px 15px rgba(0,0,0,0.2);
      animation: spin 8s linear 0s infinite forwards;
      animation-play-state: paused;
      background-image: url("../assets/singlecover.png");
      padding: 40px;
      background-repeat: no-repeat;
      background-size: 100% 100%;
    }
    .music-control {
      margin-top: 20px;
      display: flex;
      justify-content: center;
      align-items: center;
      .control-item {
        transition: all 0.3s;
        color: mediumpurple;
        width: 50px;
        display: flex;
        justify-content: center;
        align-items: center;
        margin: 0 10px;
        height: 50px;
        i {
          font-size: 22px;
        }
        border-radius: 50%;
        border: 3px solid mediumpurple;
        &.center {
          height: 70px;
          width: 70px;
          i {
            font-size: 28px;
          }
        }
        &:hover {
          background-color: mediumpurple;
          color: white;
        }
      }
    }
  }
}
.spinning {
  animation-play-state: running !important;
}
@keyframes spin {
  0% {transform: rotate(0)}
  100% {transform: rotate(360deg)}
}
.right-box {
  width: 50%;
  h2 {
    font-size: 24px;
  }
  .basic-info {
    font-size: 13px;
    font-weight: 400;
    margin: 0 10px;
    color: @font-medium-grey;
    i {
      margin-right: 5px;
      color: mediumpurple;
    }
  }
}
.lyrics-container {
  position: relative;
  overflow: hidden;
  height: 300px;
  display: flex;
  align-items: center;
  flex-direction: column;
  i {
    text-overflow: ellipsis;
    display: -webkit-box;
    -webkit-box-orient: vertical;
    -webkit-line-clamp: 1;
    transition: all 0.3s;
    font-style: normal;
    line-height: 40px;
    color: @font-medium-grey;
    &.active {
      color: mediumpurple;
      font-weight: 600;
    }
  }
}
.music-progress-full {
  width: 60%;
  height: 4px;
  background-color: #e7e7e7;
  margin-top: 15px;
  border-radius: 2px;
  display: flex;
  justify-content: flex-start;
  .music-progress {
    height: 100%;
    width: var(--scale);
    background-color: rebeccapurple;
  }
}
.pure-music {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
}
</style>