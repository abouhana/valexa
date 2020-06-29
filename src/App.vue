<template>
  <v-app id="inspire">
    <v-app-bar
            app
            clipped-right
            color="blue-grey"
            dark
    >
      <v-app-bar-nav-icon @click.stop="drawer = !drawer"></v-app-bar-nav-icon>
      <v-toolbar-title>Valexa</v-toolbar-title>
      <v-spacer></v-spacer>
    </v-app-bar>

    <v-navigation-drawer
            v-model="drawer"
            app
    >
      <v-list dense>
      </v-list>
    </v-navigation-drawer>

    <v-main>
      <v-container
              class="fill-height"
              fluid
      >
        <v-row
                justify="center"
                align="center"
        >
          <v-col class="grow">
            <LoadingPage/>
          </v-col>
        </v-row>
      </v-container>
    </v-main>

    <v-footer
            app
            color="blue-grey"
            class="white--text"
    >
      <span>Vuetify</span>
      <v-spacer></v-spacer>
      <span>&copy; 2019</span>
    </v-footer>
  </v-app>
</template>

<script>

  import ValidationProgress from "./components/ValidationProgress";
  import LoadingPage from "./pages/LoadingPage";
  import AccuracyProfile from "./components/profiles/AccuracyProfile";

  export default {
    components: {LoadingPage, ValidationProgress, AccuracyProfile},
    props: {
      source: String,
    },
    data: () => ({
      drawer: false
    }),
  }
</script>