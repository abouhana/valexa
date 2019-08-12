//import Cookies from 'js-cookie';
import {ProfilePlotCanvas} from "./__target__/canvas.js";

var vm = new Vue({
    el: "#valexa_app",
    data:{
        file:"",
        plot_id: "plot",
    },
    methods:{
        uploadFile: function(){
            this.file = this.$refs.file.files[0];
            let plot_id = this.plot_id
            let formData = new FormData();
            formData.append("file", this.file);
            axios({
                method: "POST",
                url: "http://127.0.0.1:8000/valexa_app/compute/",
                data: formData,
                headers: {
                    "Content-Type": "multipart/form-data"
                },
                responseType: 'json'
            })
            .then(function(response){
                if (!response.data) {
                    alert("File not uploaded");
                } else {
                    //let fig = response.data.figures[0];
                    let profile = response.data.profiles[0]
                    let fig = ProfilePlotCanvas(profile).figure;
                    Plotly.newPlot(plot_id, fig["data"], fig["layout"], {responsive: true});
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

