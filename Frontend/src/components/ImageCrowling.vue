<template>
  <div>
    <!-- 이미지 관련된 내용이나 기능을 담는 역할 -->
    <div class="ImageCrowling py-5">
      <!-- 그리드로 나누기 위한 컨테이너 -->
      <b-container>
        <div class="row">
          <!-- 카드 반복 생성 -->
          <div v-for="(item, index) in cards" :key="index" class="col-md-4 mb-4">
            <div class="card shadow-lg">
              <img :src="item.imageUrl" class="bd-placeholder-img card-img-top" />
              <div class="card-body">
                <div class="d-flex justify-content-end align-items-center">
                  <div class="btn-group">
                    <!-- 상세보기, 다운로드, 삭제 버튼들 -->
                    <b-button variant="outline-primary" size="sm" @click="ImageCrowlingViewDetails">상세보기</b-button>
                    <b-button variant="outline-success" size="sm" @click="ImageCrowlingDownload">다운로드</b-button>
                    <b-button variant="outline-danger" size="sm" @click="ImageCrowlingDelete">삭제</b-button>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </b-container>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import ImageCrowling from './ImageCrowling.vue';

export default {
  name: "ImageCrowling",
  components: {
    ImageCrowling,
  },
  data() {
    return {
      searchQuery: '', // 검색어를 저장하는 데이터
      images: [], // 이미지를 저장할 배열
      pageNumber: 1, // 현재 페이지 번호
      totalPage: 1, // 전체 페이지 수
      file: null, // 선택된 파일을 저장할 변수
      cards: [ // 임시 데이터 배열
        { id: 1, imageUrl: "https://source.unsplash.com/400x200/?mountain" },
        { id: 2, imageUrl: "https://source.unsplash.com/400x200/?mountain" },
        { id: 3, imageUrl: "https://source.unsplash.com/400x200/?mountain" },
        { id: 4, imageUrl: "https://source.unsplash.com/400x200/?mountain" },
        { id: 5, imageUrl: "https://source.unsplash.com/400x200/?mountain" },
        { id: 6, imageUrl: "https://source.unsplash.com/400x200/?mountain" },
        { id: 7, imageUrl: "https://source.unsplash.com/400x200/?mountain" },
        { id: 8, imageUrl: "https://source.unsplash.com/400x200/?mountain" },
        { id: 9, imageUrl: "https://source.unsplash.com/400x200/?mountain" },
      ],
    };
  },
  methods: {
    ImageCrowlingViewDetails() {
      // 상세보기 데이터 가져오는 메서드
    },
    ImageCrowlingDownload() {
      // 다운로드 데이터 가져오는 메서드
    },
    ImageCrowlingDelete() {
      // 삭제 데이터 가져오는 메서드
    }
  }
}
</script>

<style scoped>
  .oval-input {
    border-radius: 20px; /* 원하는 타원형 모양의 border-radius 값을 설정합니다 */
    padding: 10px; /* 내용물과 가장자리 간의 간격을 조정합니다 */
    width: 400px; /* 원하는 너비 값을 지정합니다 */
    outline: none; /* 포커스 효과 제거 */
    border: 1px solid #000000; /* 테두리 스타일을 지정합니다 */
    margin-bottom: 5px;
  }

</style>