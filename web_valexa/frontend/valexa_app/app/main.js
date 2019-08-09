//import Cookies from 'js-cookie';

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
                } else if (!response.data.figures) {
                    alert("No results");
                } else {
                    let fig = response.data.figures[0];
                    Plotly.newPlot(plot_id, fig["data"], fig["layout"], {responsive: true});
                    // let figid = plot_id;
                    // let fig_spec = response.data.figures[0];
                    // var element = document.getElementById(figid);
                    // if (element === null) {
                    //     throw figid + " is not a valid id";
                    // }
                    // var fig = new mpld3.Figure(figid, fig_spec);
                    // mpld3.figures.push(fig);
                    // fig.draw();
                    // return fig;
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

