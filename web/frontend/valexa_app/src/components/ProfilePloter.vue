<template>
  <div id="plots">
    <div class="profile" v-for="(profile, i) in ploterData" v-bind:key="i">
      <profile-table v-bind:levels="profile.levels"></profile-table>
      <div v-bind:id="plot_suffix+i" class="plot"></div>
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
    let i = 0;
    for (const profile of this.ploterData) {
      let fig = ProfilePlotCanvas(profile).figure;
      fig.config = { responsive: true };
      Plotly.react(this.plot_suffix + i, fig);
      i += 1;
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