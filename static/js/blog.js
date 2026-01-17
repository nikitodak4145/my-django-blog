        class BlogManager {
    // 2. КОНСТРУКТОР - вызывается при создании объекта
    constructor() {
        // 3. СВОЙСТВА объекта
        this.posts = [];  // массив статей
        this.currentPage = 1;  // текущая страница
        this.isLoading = false;  // загружается ли данные
        
        console.log("Создан новый BlogManager!");
    }
    
    // 4. МЕТОДЫ - функции объекта
    
    // Метод для загрузки статей
    loadPosts() {
        if (this.isLoading) {
            console.log("Уже загружаем...");
            return;
        }
        
        this.isLoading = true;
        console.log("Начинаем загрузку статей...");
        
        // Имитируем загрузку (позже заменим на реальный API)
        setTimeout(() => {
            this.posts = [
                {id: 1, title: "Первая статья", content: "Текст статьи 1"},
                {id: 2, title: "Вторая статья", content: "Текст статьи 2"}
            ];
            this.isLoading = false;
            console.log("Статьи загружены:", this.posts);
            this.renderPosts();  // вызываем другой метод
        }, 1000);
    }
    
    // Метод для отображения статей
    renderPosts() {
        const container = document.getElementById('posts-container');
        
        if (!container) {
            console.log("Элемент posts-container не найден!");
            return;
        }
        
        // Очищаем контейнер
        container.innerHTML = '';
        
        // Для каждой статьи создаём HTML
        this.posts.forEach(post => {
            const postElement = document.createElement('div');
            postElement.className = 'post';
            postElement.innerHTML = `
                <h3>${post.title}</h3>
                <p>${post.content}</p>
                <button onclick="blogManager.showDetails(${post.id})">
                    Подробнее
                </button>
            `;
            container.appendChild(postElement);
        });
    }
    
    // Метод для показа деталей статьи
    showDetails(postId) {
        const post = this.posts.find(p => p.id === postId);
        if (post) {
            alert(`Детали статьи:\n\n${post.title}\n\n${post.content}`);
        }
    }
    
    // Метод для добавления новой статьи
    addPost(title, content) {
        const newPost = {
            id: this.posts.length + 1,
            title: title,
            content: content
        };
        this.posts.push(newPost);
        console.log("Статья добавлена:", newPost);
        this.renderPosts();
    }
}

// 5. СОЗДАЁМ ОБЪЕКТ (экземпляр класса)
const blogManager = new BlogManager();