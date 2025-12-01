class AjaxHandler {
    constructor() {
        this.loaderElement = this.createLoader();
        this.requestCount = 0;
    }

    createLoader() {
        const loader = document.createElement('div');
        loader.innerHTML = `
            <div style="
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                background: rgba(13, 17, 23, 0.9);
                backdrop-filter: blur(8px);
                display: none;
                justify-content: center;
                align-items: center;
                z-index: 9999;
            " id="ajax-loader">
                <div style="
                    background: #1a1f2e;
                    padding: 50px 40px;
                    border-radius: 16px;
                    box-shadow: 0 25px 50px rgba(0, 0, 0, 0.5);
                    border: 1px solid #2d3748;
                    text-align: center;
                    min-width: 200px;
                    position: relative;
                    overflow: hidden;
                ">
                    <div style="
                        position: absolute;
                        top: 0;
                        left: 0;
                        width: 100%;
                        height: 3px;
                        background: linear-gradient(90deg, #4fd1c7, #667eea, #f093fb);
                        animation: shimmer 2s infinite;
                    "></div>
                    
                    <div style="
                        width: 70px;
                        height: 70px;
                        position: relative;
                        margin: 0 auto 25px auto;
                    ">
                        <div style="
                            width: 100%;
                            height: 100%;
                            border: 3px solid #2d3748;
                            border-top: 3px solid #4fd1c7;
                            border-right: 3px solid #667eea;
                            border-bottom: 3px solid #f093fb;
                            border-radius: 50%;
                            animation: spin 1.5s linear infinite;
                        "></div>
                        <div style="
                            position: absolute;
                            top: 50%;
                            left: 50%;
                            transform: translate(-50%, -50%);
                            width: 30px;
                            height: 30px;
                            background: #1a1f2e;
                            border-radius: 50%;
                        "></div>
                    </div>
                    
                    <div style="
                        color: #f7fafc;
                        font-weight: 700;
                        font-size: 18px;
                        margin-bottom: 8px;
                        letter-spacing: 1px;
                    ">LOADING</div>
                    <div style="
                        color: #a0aec0;
                        font-size: 13px;
                        font-weight: 300;
                    ">Your request is being processed</div>
                    
                    <div style="
                        display: flex;
                        justify-content: center;
                        gap: 4px;
                        margin-top: 20px;
                    ">
                        <div style="
                            width: 6px;
                            height: 6px;
                            background: #4fd1c7;
                            border-radius: 50%;
                            animation: bounce 1.4s infinite ease-in-out;
                            animation-delay: -0.32s;
                        "></div>
                        <div style="
                            width: 6px;
                            height: 6px;
                            background: #667eea;
                            border-radius: 50%;
                            animation: bounce 1.4s infinite ease-in-out;
                            animation-delay: -0.16s;
                        "></div>
                        <div style="
                            width: 6px;
                            height: 6px;
                            background: #f093fb;
                            border-radius: 50%;
                            animation: bounce 1.4s infinite ease-in-out;
                        "></div>
                    </div>
                </div>
            </div>
            <style>
                @keyframes spin {
                    0% { transform: rotate(0deg); }
                    100% { transform: rotate(360deg); }
                }
                @keyframes shimmer {
                    0% { transform: translateX(-100%); }
                    100% { transform: translateX(100%); }
                }
                @keyframes bounce {
                    0%, 80%, 100% {
                        transform: scale(0);
                    }
                    40% {
                        transform: scale(1);
                    }
                }
            </style>
        `;
        document.body.appendChild(loader);
        return loader.querySelector('#ajax-loader');
    }

    showLoader() {
        this.requestCount++;
        if (this.requestCount === 1) {
            this.loaderElement.style.display = 'flex';
            document.body.style.overflow = 'hidden';
        }
    }

    hideLoader() {
        this.requestCount--;
        if (this.requestCount <= 0) {
            this.requestCount = 0;
            this.loaderElement.style.display = 'none';
            document.body.style.overflow = '';
        }
    }

    async handleResponse(response) {
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        return data;
    }

    async get(url) {
        try {
            this.showLoader();
            const response = await fetch(url, {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                    'Accept': 'application/json'
                }
            });
            return await this.handleResponse(response);
        } catch (error) {
            console.error('GET Request failed:', error);
            throw error;
        } finally {
            this.hideLoader();
        }
    }

    async getWithValue(url, parameters) {
        try {
            this.showLoader();
            const queryParams = new URLSearchParams(parameters).toString();
            const fullUrl = queryParams ? `${url}?${queryParams}` : url;
            
            const response = await fetch(fullUrl, {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                    'Accept': 'application/json'
                }
            });
            return await this.handleResponse(response);
        } catch (error) {
            console.error('GET with parameters failed:', error);
            throw error;
        } finally {
            this.hideLoader();
        }
    }

    async post(url, data = null) {
        try {
            this.showLoader();
            const config = {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Accept': 'application/json'
                }
            };

            if (data) {
                config.body = JSON.stringify(data);
            }

            const response = await fetch(url, config);
            return await this.handleResponse(response);
        } catch (error) {
            console.error('POST Request failed:', error);
            throw error;
        } finally {
            this.hideLoader();
        }
    }

    async postWithJSON(url, jsonData) {
        return this.post(url, jsonData);
    }
}

const ajax = new AjaxHandler();