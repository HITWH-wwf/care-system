<template>
    <div class="big" style="width:100%">
        
        <div class="content" style="overflow: hidden;">
           
             
            <img src="@/assets/sunset.jpg" alt="bgimage" class="bgImage"/>
           <div  id="title" >
                欢迎使用

            
               <!-- <div class="img1">
                    <img src="static/33.png" >
                    Working
                </div> -->
                
            </div>
            
        </div>
        <!-- <div class="container">
                <div>
                    <img src="static/44.png" class="img1">
                   
                </div>
                
                <div>
                    <img src="static/66.png" class="img2">
                   
                </div>
            </div> -->
            
        <footer>《版权所有&copy;哈工大威海</footer>    
    </div>

</template>

<script>



export default {
    data() {
        return {
        }
    },
    components: {
        
    }
    
}



</script>

<style lang="scss" scoped>
.big{
  background-color: #99a9bf;
  
}
.content {
    top: 60px;

} 
.bgImage{
    position: relative;
	overflow: hidden;
	
	padding-left: -40px;
        display: block;
        width: 100%;
        height: 46rem;
        transform: perspective(62.5rem) translateZ(0);
        transition:  8s;
        &:hover {
             transform: perspective(62.5rem) translateZ(6.25rem);
             transition:  8s;
         }
    }

 #title {
        font-family: Georgia, "Microsoft YaHei", "微软雅黑",  STXihei, "华文细黑",  serif;
        color: #fff;
        text-align: center;
        font-size: 3.125rem;
        width: 31.25rem;
        height: 3.125rem;
        position: absolute;
        top: 50%;
        left: 50%;
        margin-top: -0.625rem;
        margin-left: -15.625rem;
    }
.container{
    
    display: inline;}
footer{
    position: relative;
    text-align: center;
    
    font-size: 1.3rem;
}
.img1{
        position: absolute;
        height:3rem;
        left:20rem;
    }
    #t{
        position: absolute;
        font-size:2rem;
        left:40rem;
    }
    .img2{
        position: absolute;
        height:3rem;
        left:80rem;
    }
@media screen and (max-width: 440px) {
    .bgImage {
        height: 18rem !important;
    }
    #title {
        font-size: 2rem !important;
    }
}
</style>