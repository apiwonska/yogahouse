const hasPagination = document.querySelector('#post-list-pagination');

handleForm()
if (hasPagination) handlePagination()


function getQueryParams() {
  const urlParams = new URLSearchParams(window.location.search);
  const catParam = urlParams.get('cat') || '';
  const qParam = urlParams.get('q') || '';
  const orderParam = urlParams.get('order') || '';
  const pageParam = urlParams.get('page') || '';
  return { qParam, catParam, orderParam, pageParam };
}

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
  const inputText = document.querySelector('#searchText');
  const selectCategoryOptions = document.querySelectorAll('#inputCategory option'); 
  const selectOrderOptions = document.querySelectorAll('#inputOrder option');
  const {qParam, catParam, orderParam} = getQueryParams();

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

function handlePagination() {
  const prevPage = document.querySelector('#previous-page');
  const pages = document.querySelectorAll('.pagination-page');
  const nextPage = document.querySelector('#next-page');
  const { qParam, catParam, orderParam, pageParam } = getQueryParams();

  const injectQueryParams = (a) => {
    const prevQueryString = a.getAttribute('href');
    const addition = (qParam && `&q=${qParam}`) + 
                    (catParam && `&cat=${catParam}`) + 
                    (orderParam && `&order=${orderParam}`);
    a.setAttribute('href', prevQueryString + addition);
  }

  if (prevPage) injectQueryParams(prevPage);
  if (nextPage) injectQueryParams(nextPage);
  pages.forEach((page) => {
    injectQueryParams(page);
    if (
      page.textContent.trim() === pageParam ||
      (!pageParam && page.textContent.trim() === '1')
    ) {
      page.classList.add('page-active');
    }
  });
}