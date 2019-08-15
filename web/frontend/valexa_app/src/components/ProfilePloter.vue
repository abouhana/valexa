<template>
  <div id="plots">
    <div class="profile" v-for="(profile, i) in ploterData" v-bind:key="i">
      <profile-table v-bind:profile="profile"></profile-table>
      <div v-bind:id="plot_suffix+i" class="plot"></div>
      <img v-bind:id="'export'+i">
    </div>
  </div>
</template>

<script>
import { ProfilePlotCanvas } from "../ploting/__target__/canvas.js";
import Plotly from "plotly.js";
import ProfileTable from "./ProfileTable";

export default {
  name: "ProfilePloter",
  props: {
    ploterData: Array
  },
  components: {
    ProfileTable,
  },
  data() {
    return {
      plot_suffix: "plot_"
    };
  },
  updated() {
    var i = -1;

    for (const profile of this.ploterData) {
      i += 1;
      let fig = ProfilePlotCanvas(profile).figure;
      let img_jpg = document.getElementById('export' + i);
      fig.config = { responsive: true };
      Plotly.react(
        this.plot_suffix + i, fig
      )
      .then(function(gd) {
        Plotly.toImage(
          gd, 
          {height: gd.offsetHeight, width: gd.offsetWidth}
        )
        .then(function(url) {
              img_jpg.src = url;
              gd.innerHTML = "";
              //return Plotly.toImage(gd,{format:'jpeg',height:400,width:400});
          })
      });
    }
  }
};
</script>

<style scoped>
#plots {
  max-width: 1000px;
  margin-left: auto;
  margin-right: auto;
}
.profile {
  margin-top: 5vw;
}
</style>