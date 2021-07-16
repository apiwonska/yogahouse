handleForm()
handlePagination()

function handleForm() {
  const selectCategory = document.querySelector('#inputCategory');
  const selectCategoryOptions = document.querySelectorAll('#inputCategory option');  
  const selectOrder = document.querySelector('#inputOrder');
  const selectOrderOptions = document.querySelectorAll('#inputOrder option');  

  handleInputValuesAndAttributesOnLoad();
  handleChangeSelectOption(selectCategory, selectCategoryOptions);
  handleChangeSelectOption(selectOrder, selectOrderOptions);
}

function handleInputValuesAndAttributesOnLoad() {
  const urlParams = new URLSearchParams(window.location.search);
  const catParam = urlParams.get('cat') || '';
  const qParam = urlParams.get('q') || '';
  const orderParam = urlParams.get('order') || '';
  const inputText = document.querySelector('#searchText');
  const selectCategoryOptions = document.querySelectorAll('#inputCategory option'); 
  const selectOrderOptions = document.querySelectorAll('#inputOrder option');

  window.addEventListener('load', () => {
    inputText.value = qParam;
    selectCategoryOptions.forEach((option) => {
      if (option.value === catParam) {
        option.setAttribute('aria-selected', 'true');
        option.setAttribute('selected', 'true');
      } else {
        option.setAttribute('aria-selected', 'false');
        option.removeAttribute('selected');
      }
    });
    selectOrderOptions.forEach((option) => {
      if (option.value === orderParam) {
        option.setAttribute('aria-selected', 'true');
        option.setAttribute('selected', 'true');
      } else {
        option.setAttribute('aria-selected', 'false');
        option.removeAttribute('selected');
      }
    });
  });
}

function handleChangeSelectOption(selectInput, selectOptions) {
  selectInput.addEventListener('change', (e) => {
    selectOptions.forEach((option) => {
      if (option.value === e.target.value) {
        option.setAttribute('aria-selected', 'true');
        option.setAttribute('selected', 'selected');
      } else {
        option.setAttribute('aria-selected', 'false');
        option.removeAttribute('selected');
      }
    });
  });
}


// function handlePagination() {
//   const pagination = document.querySelector('#post-list-pagination');
//   console.log('pagination', pagination);

// }





