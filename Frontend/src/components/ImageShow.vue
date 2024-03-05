<!-- DB에서 받아온 상세 내용 보여주는 곳
이미지 크롤링과 생성 모두 이 컴포넌트로 보여줄지는 고민
1. 이미지
2. 기타 데이터 -->

<template>
    <b-modal v-model="showModal" title="Image Details">
      <div v-if="imageInfo">
        <!-- 이미지 표시 -->
        <img :src="imageInfo.imageUrl" alt="Image" style="max-width: 100%; max-height: 400px;">
  
        <!-- 다른 상세 정보들 -->
        <div>
          <!-- 이미지 URL -->
          <p>Image URL: {{ imageInfo.imageUrl }}</p>
          
          <!-- 다른 상세 정보들 -->
          <p>Other Detail: {{ imageInfo.otherDetail }}</p>
          <!-- 필요한 다른 상세 정보들을 표시 -->
        </div>
      </div>
    </b-modal>
  </template>
  
  <script>
  import axios from 'axios';
  
  export default {
    props: {
      showModal: {
        type: Boolean,
        required: true
      },
      imageInfo: {
        type: Object,
        required: true
      }
    },
    data() {
      return {
        // 이미지의 상세 정보를 저장할 객체
        detailedInfo: null
      };
    },
    watch: {
      imageInfo: {
        immediate: true,
        handler(newVal) {
          // 이미지 정보가 변경되면 API를 통해 상세 정보를 가져옴
          this.fetchDetailedInfo(newVal);
        }
      }
    },
    methods: {
      async fetchDetailedInfo(imageInfo) {
        if (imageInfo) {
          try {
            // 이미지의 상세 정보를 가져오는 API 요청을 보냄
            const response = await axios.get(`https://quotes.api.thegam.io/create_image/results/{id}`);
            this.detailedInfo = response.data;
          } catch (error) {
            console.error('Error fetching detailed information:', error);
            // 에러 처리
          }
        }
      }
    }
  }
  </script>
  