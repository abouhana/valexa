<template>
  <div id="file-upload">
    <div id="drop" 
      @dragenter="handleDragover" 
      @dragover="handleDragover"
      @drop="handleDrop">
        Drop a spreadsheet file here to see sheet data
    </div>
      <input type="file" id="file" 
        v-on:change="uploadFile($event.target.files)" 
      /> ... or click here to select a file
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: 'FileUpload',
  props: {
    url: String,
  },
  methods:{
        handleDrop(e) {
          e.stopPropagation();
          e.preventDefault();
          this.uploadFile(e.dataTransfer.files);
        },
        handleDragover(e) {
          e.stopPropagation();
          e.preventDefault();
          e.dataTransfer.dropEffect = 'copy';
        },
        uploadFile: function(files){
            this.file = files[0];
            var vm = this;
            let formData = new FormData();
            formData.append("file", this.file);
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
                vm.$emit("fileupload-success", response);
            })
            .catch(function(error){
                vm.$emit("fileupload-error", error);
            })
            .finally(function(){
                event.target.value = "";
                //event.target.type = "file";
            })
        }
    }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
#drop{
	border:2px dashed #bbb;
	-moz-border-radius:5px;
	-webkit-border-radius:5px;
	border-radius:5px;
	padding:25px;
	text-align:center;
	font:20pt bold,"Vollkorn";
  color:#bbb;
  max-width: 1000px;
  margin-left: auto;
  margin-right: auto;
}
a { 
  text-decoration: none 
}
</style>
