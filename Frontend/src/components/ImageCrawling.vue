<template>
  <div>
    <!-- 반응형 디자인 지원 -->
    <b-container>
      <!-- 이미지 키워드 입력창, 카테고리 선택, 신규 크롤링 버튼 모음 -->
      <!-- 버튼들을 왼쪽 정렬 -->
      <div class="row justify-content-left mb-3 mt-3">
        <div class="col-md-7">
          <!-- 검색창 스타일 지원 -->
          <div class="search-bar">
            <b-form no-ok no-cancel class="d-flex align-items-center">
              <b-form-input id="prompt" v-model="prompt" size="lg" placeholder="단어를 입력해 주세요"></b-form-input>
              <div class="mx-1"></div>
              <!-- 카테고리 선택 -->
              <b-dropdown size="lg" v-model="selectedCategory" :text="selectedCategory ? selectedCategory : '카테고리 선택'" variant="outline-primary" :class="{'invalid-dropdown': !selectedCategory}">
                <b-dropdown-menu class="custom-dropdown-menu">
                  <div style="max-height: 300px; overflow-y: auto;">
                    <!-- 백엔드에서 가져온 카테고리 데이터를 반복하여 드롭다운 메뉴 -->
                    <b-dropdown-item v-for="category in categories" :key="category.id" @click="selectCategory(category)">{{ category.category }}</b-dropdown-item>
                  </div>
                </b-dropdown-menu>
              </b-dropdown>
              <div class="mx-1"></div>
              <b-button type="submit" variant="primary" class="ml-3" size="lg" style="white-space: nowrap;" @click="submitForm">신규 크롤링</b-button>
              <div class="mx-1"></div>
              <b-button type="button" variant="primary" class="ml-3" size="lg" style="white-space: nowrap;" @click="submitFormCheck">조회</b-button>
            </b-form>
          </div>
        </div>
        <!-- 전체 선택 체크박스 -->
        <div class="col-md-5 d-flex justify-content-end align-items-center">
          <div class="checkbox-container">
            <b-form-checkbox size="lg" v-model="selectAll" @change="selectAllImages" class="mr-2">전체 선택</b-form-checkbox>
            <!-- 선택된 이미지 다운로드 버튼 -->
            <b-button variant="success" @click="downloadSelectedImages" size="lg" :disabled="selectedImages.length === 0">선택된 이미지 다운로드</b-button>
            <!-- 선택된 이미지 삭제 버튼 -->
            <b-button variant="danger" @click="deleteSelectedImages" size="lg" :disabled="selectedImages.length === 0">선택된 이미지 삭제</b-button>
          </div>
        </div>
      </div>
      <!-- 이미지 관련된 내용이나 기능을 담는 역할 -->
      <div class="ImageCrawling py-7">
        <!-- 그리드로 나누기 위한 컨테이너 -->
        <div class="row">
          <!-- 카드 반복 생성 -->
          <div v-for="content in contents" :key="content.image_id" class="col-md-3 mb-3">
            <div class="card shadow-lg">
              <div class="card-body">
                <!-- 이미지 -->
                <b-img :src="content.imageURL" class="image" alt="이미지 설명" thumbnail fluid />
                <div class="d-flex justify-content-between align-items-center mt-3">
                  <!-- 체크 박스 -->
                  <div class="mr-2">
                    <b-form-checkbox size="lg" v-model="selectedImages" :value="content.image_id"></b-form-checkbox>
                  </div>
                  <div class="btn-group">
                    <!-- 상세보기, 다운로드, 삭제 버튼들 -->
                    <b-button variant="outline-primary" size="sm" @click="viewImageDetail(content)">상세보기</b-button>
                    <b-button variant="outline-success" size="sm" @click="downloadImage(content.imageURL)">다운로드</b-button>
                    <b-button variant="outline-danger" size="sm" @click="confirmDeleteImage(content.image_id)">삭제</b-button>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </b-container>

    <div v-if="isLoading" class="inner-contspainer">
      <b-spinner v-if="isLoading"></b-spinner>
    </div>   

    <!-- 페이지네이션 -->
    <div class="d-flex justify-content-end">
      <div>
        <b-button @click="changePage(pageNumber - 1)" :disabled="pageNumber <= 1">이전 페이지</b-button>
        <span>{{ pageNumber }} / {{ totalPage }}</span>
        <b-button @click="changePage(pageNumber + 1)" :disabled="pageNumber >= totalPage">다음 페이지</b-button>
      </div>
    </div>
    <!-- 상세보기 모달 창 -->
    <ImageCrawlingViewDetail ref="modalViewDetail" :imageInfo="selectedImageInfo" />
  </div>
</template>

<script>
import axios from 'axios';
import ImageCrawlingViewDetail from './ImageCrawlingViewDetail.vue';

export default {
  components: {
    ImageCrawlingViewDetail
  },
  data() {
    return {
      prompt: '',
      selectedCategory: null,
      selectedImageInfo: null,
      categories: [], // 카테고리를 담는 배열
      contents: [], // 이미지 정보를 담는 배열
      pageNumber: 1, // 현재 페이지 번호
      totalPage: 0, // 전체 페이지 수
      selectedImages: [], // 선택된 이미지를 추적하는 배열
      selectAll: false, // 전체 선택 체크박스
      isLoading: false,
    };
  },

  created() {
    // 이미지 데이터를 가져오는 API 호출
    this.fetchImages();
    this.fetchCategories(); // 카테고리 데이터 가져오기
  },

  methods: {
  async fetchImages() {
    try {
      const response = await axios.get(`https://quotes.api.thegam.io/pixabay/`);
      this.contents = response.data.contents;
      this.totalPage = response.data.total_page;
      this.pageNumber = 1; // totalPage를 가져왔으므로 페이지 번호를 1로 설정합니다.
    } catch (error) {
      console.error('Error fetching images:', error);
    }
  },                                    

  async deleteImage(imageId) {
    try {
      await axios.delete(`https://quotes.api.thegam.io/pixabay/delete/?ids=${imageId}`);
      // 이미지 삭제 후 다시 이미지 데이터를 불러오기
      this.fetchImages();
    } catch (error) {
      console.error('Error deleting image:', error);
    }
  },

  // 모달을 열기 위한 메서드
  viewImageDetail(image) {
    this.selectedImageInfo = image; // 선택된 이미지 정보 설정
    this.$refs.modalViewDetail.open(); // 모달 창 열기
  },

  downloadImage(imageURL) {
    axios.get(imageURL, { responseType: 'blob' })
      .then(response => {
        const blob = new Blob([response.data], { type: response.headers['content-type'] });
        const downloadLink = document.createElement('a');
        downloadLink.href = URL.createObjectURL(blob);
        downloadLink.download = 'image';
        document.body.appendChild(downloadLink);
        downloadLink.click();
        document.body.removeChild(downloadLink);
      })
        .catch(error => {
        console.error('Error downloading image:', error);
      });
  },

  // 전체 선택 체크박스 변경 이벤트 핸들러
  selectAllImages() {
    // 전체 선택 체크박스의 상태에 따라 선택 여부를 설정합니다.
    this.selectedImages = this.selectedImages.length === this.contents.length ? [] : this.contents.map(content => content.image_id);
  },

  // 카테고리 선택 함수
  selectCategory(category) {
    this.selectedCategory = category.category;
  },

  // 카테고리 데이터 불러오기
  async fetchCategories() {
    try {
      const response = await axios.get('https://quotes.api.thegam.io/pixabay/image_categories/');
      this.categories = response.data; // 카테고리 배열에 데이터 저장
    } catch (error) {
      console.error('Error fetching categories:', error);
    }
  },

  // 이미지 검색 및 카테고리 선택 폼 제출 처리
   async submitForm() {
    try {
      // 사용자가 입력한 키워드와 카테고리를 포함하여 신규 크롤링 요청 보내기
      const url = `https://quotes.api.thegam.io/pixabay/?keyword=${this.prompt}&category=${this.selectedCategory}&crawling_on=1`;
      
      // Axios를 사용하여 HTTP GET 요청 보내기
      const response = await axios.get(url);
      
      // 요청이 성공했을 때의 처리
      console.log('응답 데이터:', response.data);
      this.isLoading = true;
      await this.fetchImages(); // 이미지를 다시 불러옴
      window.location.reload();
    } catch (error) {

      // 요청이 실패했을 때의 처리
      console.error('요청 실패:', error);
    } finally {
      this.isLoading = false;
    }
  },

  submitFormCheck() {
    // 사용자가 입력한 키워드와 카테고리를 포함하여 신규 크롤링 요청 보내기
    const url = `https://quotes.api.thegam.io/pixabay/?keyword=${this.prompt}&category=${this.selectedCategory}&crawling_on=0&p=${this.pageNumber}`;

    // Axios를 사용하여 HTTP POST 요청 보내기
    axios.get(url)
      .then(response => {
        // 요청이 성공했을 때의 처리
        console.log('응답 데이터:', response.data);
        // 이미지 신규 크롤링 요청에 대한 응답이 성공했을 때 이미지를 다시 불러옴
          this.contents = response.data.contents;
          this.totalPage = response.data.total_page;
          this.pageNumber = 1;
      })
      .catch(error => {
        // 요청이 실패했을 때의 처리
        console.error('요청 실패:', error);
      });
  },
    
  async changePage(page) {
    // 페이지 번호가 1보다 작으면 1로 설정
    if (page < 1) {
      page = 1;
    }

    // 페이지 번호가 totalPage를 초과하면 totalPage로 설정
    if (page > this.totalPage) {
      page = this.totalPage;
    }

    try {
      let url = `https://quotes.api.thegam.io/pixabay/?p=${page}`;
      if (this.prompt && this.selectedCategory) {
        url += `&keyword=${this.prompt}&category=${this.selectedCategory}&crawling_on=0`; // 키워드와 카테고리 정보 추가
      }
      const response = await axios.get(url);
      this.contents = response.data.contents;
      this.totalPage = response.data.total_page;
      this.pageNumber = page;
    } catch (error) {
      console.error('Error fetching images:', error);
    }
  },

  // 선택된 이미지 다운로드 함수
  downloadSelectedImages() {
    // 선택된 이미지가 없으면 함수 종료
    if (this.selectedImages.length === 0) {
      console.log('선택된 이미지가 없습니다.');
      return;
      }
    // 선택된 이미지의 URL을 순회하면서 이미지를 다운로드합니다.
    this.selectedImages.forEach(imageId => {
      const imageURL = this.contents.find(content => content.image_id === imageId).imageURL;
      this.downloadImage(imageURL);
    });
  },

  // 이미지 삭제 확인 후 삭제 진행
  confirmDeleteImage(imageId) {
    // 관리자에게 이미지 삭제 여부를 확인하는 경고창을 띄웁니다.
    const confirmed = confirm('이미지를 삭제하시겠습니까?');

    // 사용자가 확인을 선택한 경우에만 이미지 삭제를 진행합니다.
    if (confirmed) {
      this.deleteImage(imageId);
    }
  },
 
  // 선택된 이미지 삭제 함수
  async deleteSelectedImages() {
    // 선택된 이미지가 없으면 함수 종료
    if (this.selectedImages.length === 0) {
      console.log('선택된 이미지가 없습니다.');
      return;
    }

    // 관리자가 삭제를 확인하는 경고창을 띄웁니다.
    const confirmed = confirm('선택된 이미지를 삭제하시겠습니까?');

    // 관리자가 확인을 선택한 경우에만 이미지 삭제를 진행합니다.
    if (confirmed) {
      try {
        // 선택된 이미지들의 ID 배열
        const selectedImageIds = this.selectedImages;

        // 삭제할 이미지들의 ID를 서버에 전송하여 삭제
        const apiUrl = 'https://quotes.api.thegam.io/pixabay/delete/';
        const queryString = selectedImageIds.map(id => `ids=${id}`).join('&');
        const deleteUrl = `${apiUrl}?${queryString}`;
        await axios.delete(deleteUrl);

        // 선택된 이미지들을 화면에서 제거
        this.selectedImages = [];

        // 이미지 삭제 후 다시 이미지 데이터를 불러오기
        this.fetchImages();
        this.selectAll = false; // 전체 선택 체크 해제
      } catch (error) {
        console.error('Error deleting images:', error);
      }
    } else {
      console.log('삭제가 취소되었습니다.');
    }
  },
}}
</script>

<style scoped>
.image {
  width: 100%; /* 이미지의 너비를 100%로 설정하여 부모 요소에 맞춤 */
  height: 200px; /* 높이를 자동으로 조정하여 원본 이미지의 종횡비를 유지 */
  object-fit: cover; /* 이미지가 자리를 차지하도록 설정 */
}

.spinner-container {
  position: fixed; /* 고정 위치 */
  top: 0;
  left: 0;
  width: 100%; /* 화면 전체 너비 */
  height: 100%; /* 화면 전체 높이 */
  background-color: rgba(255, 255, 255, 0.7); /* 반투명 배경 */
  display: flex; /* Flexbox를 사용하여 중앙 정렬 */
  justify-content: center; /* 가로 방향 중앙 정렬 */
  align-items: center; /* 세로 방향 중앙 정렬 */
  z-index: 9999; /* 다른 요소들 위에 표시 */
  }

</style>