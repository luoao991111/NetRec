<template>
  <div class="carousel-wrapper">
<!--    <input type="radio" name="carousel-control"-->
<!--    v-for="(control, index) in items"-->
<!--    :checked="index === displayItemIdx"-->
<!--    />-->
    <Billboard class="carousel-item"
        v-for="(item, index) in items"
        :data="item"
        :style="{left: (50 * index - 25) + '%',
                  backgroundColor: color[index + 1],
                  transform: 'translateX(' + 100 * (displayItemIdx - defaultItemIdx) + '%)'
                  }">

    </Billboard>
    <div class="carousel-control carousel-left" @click="displayItemIdx ++"
    v-if="displayItemIdx < items.length - 1">
      <i class="fa fa-chevron-left"/>
    </div>
    <div class="carousel-control carousel-right" @click="displayItemIdx --"
    v-if="displayItemIdx > 0">
      <i class="fa fa-chevron-right"/>
    </div>
  </div>
</template>

<script>
import Billboard from "@/components/Home/Billboard";
export default {
  name: "Carousel",
  components: {Billboard},
  data () {
    return {
      displayItemIdx: 1,
      defaultItemIdx: 1,
      color: ['#FBADAF', '#ECB7D4', '#91D3E1', "#FBADAF"],
      items: [
        {
          text: "Happier Than Ever",
          imgurl: require('../../assets/happierthanever.jpg'),
          desc: ["Happier Than Ever is the upcoming second studio album by American singer and songwriter Billie Eilish, scheduled to be released on July 30, 2021, by Darkroom and Interscope Records. It follows Eilish's 2019 debut album, When We All Fall Asleep, Where Do We Go?."],
          time: "2020 – January 2021",
          originURL: "https://www.nme.com/news/music/billie-eilish-announces-happier-than-ever-2022-world-tour-dates-2946067"
        },
        {
          text: "Pale Blue",
          imgurl: require('../../assets/paleblue.jpg'),
          desc: ["※特典は「先着」となり、数に限りがあります。一部の店舗/ECサイトでは特典が付かない場合がございます",
          "ご予約ご購入の際は、特典の有無を必ず店頭/ECサイトでご確認下さい。"],
          time: "2021-05-31",
          originURL: "https://music.163.com/#/album?id=127827934"
        },
        {
          text: "ハートフォレスト",
          imgurl: require('../../assets/heart.jpg'),
          desc: ["こちらはスマートフォンゲーム『アークナイツ』のイメージソングに起用されており、小倉の柔らかな歌声に包まれるような暖かみのあるハートフルな１曲。身の回り「優しさ」や「感謝」、そして困難を超えた先にある「希望」をテーマとした、明るく前向きな気持ちになれる歌詞にもぜひ注目して聴いて欲しい"],
          originURL: "https://y.qq.com/n/ryqq/albumDetail/002pqx1X3cLm0M"
        }
      ]
    }
  }
}
</script>

<style scoped>
.carousel-wrapper {
  list-style: none;
  width: 80%;
  overflow: hidden;
  display: flex;
  justify-content: center;
  min-height: 500px;
  z-index: 1;
}
.carousel-wrapper:after {
  content: "";
  display: block;
  clear: both;
}
div.carousel-item {
  width: 50%;
  position: absolute;
  transition: all 0.3s ease-in-out;
}
.carousel-control {
  position: absolute;
  color: #989898;
  font-size: 30px;
  width: 50px;
  height: 50px;
  font-weight: 200;
  display: flex;
  justify-content: center;
  align-items: center;
  top: 220px;
  z-index: 1;
}
.carousel-control >i {
  margin: auto;
}
.carousel-control:before {
  content: "";
  display: block;
  position: absolute;
  top: 0; right: 0; bottom: 0; left: 0;
  border-radius: 50%;
  backdrop-filter: blur(2px);
  background-color: rgba(255, 255, 255, 0.2);
  box-shadow: 0 25px 50px rgba(0, 0, 0, 0.2);
  z-index: -1;
}
.carousel-left {
  left: 10%;
}
.carousel-right {
  right: 10%;
}
</style>