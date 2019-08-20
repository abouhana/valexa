<template>
  <div id="file-upload">
    <form @submit.prevent="uploadFile">
      <div class="container">
        <div id="drop" 
          @dragenter="handleDragover" 
          @dragover="handleDragover"
          @drop="handleDrop">
            <div v-if="!files">Drop a spreadsheet here</div>
            <div v-else>Ready</div>
        </div>
        <div class="btn-file">
          <label for="file" class="file-input">
            <p v-if="!files">Or select a file</p> 
            <p v-else>{{$refs.file.files[0].name}}</p> 
            <input type="file" id="file" ref="file" required
            @change="files = $event.target.files">
          </label>
        </div>
        <div class="spacer"></div>
        <div id="profile-parameters" class="container">
          <div class="parameter">
            <input type="text" v-model="acceptance"> Acceptance limit
          </div>
          <div class="parameter">
            <input type="text" v-model="tolerance"> Tolerance limit
          </div>
          <div class="parameter">
            <input type="text" v-model="coumpound_name"> Coumpound name
          </div>
          <div class="parameter">
            <button type="submit">evaluate</button>
          </div>
        </div>
      </div>
    </form>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: 'FileUpload',
  props: {
    url: String,
  },
  data() {
    return {
      "files": null,
      "acceptance": 20,
      "tolerance": 80,
      "coumpound_name": "",
    };
  },
  methods:{
        handleDrop(e) {
          e.stopPropagation();
          e.preventDefault();
          this.$refs.file.files = e.dataTransfer.files;
          this.files = e.dataTransfer.files;
        },
        handleDragover(e) {
          e.stopPropagation();
          e.preventDefault();
          e.dataTransfer.dropEffect = 'copy';
        },
        uploadFile: function(){
            let file = this.files[0];
            var vm = this;
            let formData = new FormData();
            formData.append("file", file);
            formData.append("acceptance", this.acceptance);
            formData.append("tolerance", this.tolerance);
            axios({
                method: "POST",
                url: vm.url,
                data: formData,
                headers: {
                    "Content-Type": "multipart/form-data"
                },
                responseType: 'json'
            })
            .then(function(response){
                vm.$emit(
                  "fileupload-success",
                  { "data": response.data,
                    "filename": file.name,
                  }
                );
            })
            .catch(function(error){
                vm.$emit("fileupload-error", error);
            })
            .finally(function(){
                vm.$refs.file.value = "";
                vm.$refs.file.files = null;
                vm.files = null;
            })
        }
    }
}
</script>

<style scoped>
.container{
  display: grid;
  max-width: 1000px;
  margin: auto;
}

.spacer{
  height: 5vh;
  width: 100%;
}

a { 
  text-decoration: none 
}

#file-upload{
  text-align:center;
}

#drop{
	border:2px dashed #bbb;
	-moz-border-radius:5px;
	-webkit-border-radius:5px;
	border-radius:5px;
	padding:25px;
	text-align:center;
	font:20pt bold,"Vollkorn";
  color:#bbb;
  grid-row-start: 1;
}

.btn-file{
  grid-row-start: 2;
  grid-column-start: 1;
  width: 60%;
  margin: auto;
}
.file-input{
  margin: auto;
  align-items: center;
  width: 100%;
  height: 5vh;
  background-color: rgb(230,230,230);
  border-style: solid;
  border-radius: 5px;
  display: flex;
}
.file-input p{
  margin: auto;
}
.file-input input{
  display:none;
}

#profile-parameters{
  display: flexbox;
  margin: 0;
}
.parameter{
  display: inline-flex;
}
.parameter input{
  border: 1px solid;
  border-style: solid;
  border-radius: 5px;
  margin-right: 1vw;
  text-align: center;
}
.parameter button{
  width: 171px;
  margin-top: 1vh;
}
</style>
