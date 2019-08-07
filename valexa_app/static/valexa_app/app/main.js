//import Cookies from 'js-cookie';

var vm = new Vue({
    el: "#valexa_app",
    data:{
        file:""
    },
    methods:{
        uploadFile: function(){
            this.file = this.$refs.file.files[0];
            let formData = new FormData();
            formData.append("file", this.file);
            axios.post("http://127.0.0.1:8000/valexa_app/compute/", formData,
            {
                headers: {
                    "Content-Type": "multipart/form-data"
                }
            })
            .then(function(response){
                if (!response.data) {
                    alert("File not uploaded");
                } else if (!response.data.results) {
                    alert("No results");
                } else {
                    alert("File uploaded");
                }
            })
            .catch(function(error){
                console.log(error);
            })
        }
    }
})

axios.defaults.headers.common['X-CSRFTOKEN'] = Cookies.get('csrftoken');
axios.defaults.headers.common['X-Requested-With'] = 'XMLHttpRequest';
