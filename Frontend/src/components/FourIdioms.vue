<template>
  <div>
    <div class="black-bg" v-if="modal_open == true">
    <div class="white-bg">
      <h4>등록및수정</h4>
      <p>Create.vue 내용</p>
      <button @click="modal_open = false">닫기</button>
    </div>
    </div>
    <div>
      <b-dropdown id="dropdown-1" text="Dropdown Button" class="m-md-2">
        <b-dropdown-item>First Action</b-dropdown-item>
        <b-dropdown-item>Second Action</b-dropdown-item>
        <b-dropdown-item>Third Action</b-dropdown-item>
        <b-dropdown-divider></b-dropdown-divider>
        <b-dropdown-item active>Active action</b-dropdown-item>
        <b-dropdown-item disabled>Disabled action</b-dropdown-item>
      </b-dropdown>
    </div>
    <b-table striped hover :items="items" :fields="fields">
      <template #cell(actions)="row">
        <!-- 제어 버튼 -->
        <div class="btn-group" role="group">
          <b-button size="sm" @click="row.toggleDetails">
          {{ row.detailsShowing ? '숨김' : '펼침' }}
        </b-button>
        <b-button size="sm" @click="info(row.item, row.index, $event.target)" class="mr-1">
          수정
        </b-button>
          <b-button size="sm" variant="danger" @click="deleteItem(row.item)">삭제</b-button>
        </div>
      </template>
    </b-table>
  </div>
</template>
  
  <script>
  import axios from 'axios';

    export default {
      data() {
        // let items = response.data.content.sort((a,b) => {return b.id - a.id})
        return {
          fields:[
            {
              key: 'id',
              label: 'No'
            },
            {
              key: 'category',
              label: '카테고리'
            },
            {
              key: 'contents_kr',
              label: '사자성어(한글)'
            },
            {
              key: 'contents_zh',
              label: '사자성어(한문)'
            },
            {
              key: 'contents_detail',
              label: '뜻풀이'
            },
            {
              key: 'actions',
              label: '제어',
              class: 'text-center',
              thClass: 'text-center',
              sortable: false,
              formatter: this.formatActions,
            },
          ],
          items: [],
          modal_open: false
        };
      },
      created(){
        // FastAPI 서버의 URL
        const apiUrl = 'https://quotes.api.thegam.io/fourchar/';
  
        // Axios를 사용하여 GET 요청을 보냄
        axios.get(apiUrl)
          .then(response => {
          // 받은 데이터를 Vue 데이터에 저장
          this.items = response.data.content;
        })
        .catch(error => {
          console.error('데이터를 불러오는 중 오류 발생:', error);
        });
      },
      methods: {
        formatActions(value, key, item){
          return `
            <div class="btn-group" role="group">
              <b-button size="sm" variant="primary" @click="openItem(item)">펼침</b-button>
              <b-button size="sm" variant="primary" @click="editItem(item)">수정</b-button>
              <b-button size="sm" variant="danger" @click="deleteItem(item)">삭제</b-button>
            </div>
          `;
        },
        openItem(item) {
          // 펼침 버튼을 누를 때 수행할 동작 정의
        },
        editItem(item) {
          modal_open = true
        },
        deleteItem(item) {
          // 삭제 버튼을 누를 때 수행할 동작 정의
        },
      }
    }
  </script>
<style>
body {
  margin: 0
}
div {
  box-sizing: border-box;
}
.black-bg {
  width: 100%; height: 100%;
  background: rgba(0,0,0,0.5);
  position: fixed; padding: 20px;
}
.white-bg{
  width: 100%; background: white;
  border-radius: 8px;
  padding: 20px;
}
</style>