// Instale o pacote node-fetch: npm install node-fetch
const express = require('express');
const app = express();
const PORT = 3000;

const API_ID = '28af4c45232b4f8f84a300e56269bc24'
const APP_KEY = '93d7a5c1cc46450983bd48df34cb7904'

app.get('/api/data', async (req, res) => {
    const foodName = req.query.foodName;
    
    try {
        const url = 'https://api.nutritionix.com/v1_1/search/${foodName}?results=0%3A1&fields=item_name%2Citem_id%2Cbrand_name%2Cnf_calories%2Cnf_total_fat%2Cnf_protein%2Cnf_total_carbohydrate&appId=${API_ID}&appKey=${APP_KEY}';
        const response = await fetch(url, { method: 'GET' });
        const data = await response.json();
        res.json(data); // Retorna os dados para o cliente
    } catch (error) {
        console.error('Erro ao fazer a requisição:', error);
        res.status(500).json({ error: 'Erro ao obter dados do servidor' });
    }
});

app.listen(PORT, () => {
    console.log(`Servidor intermediário rodando na porta ${PORT}`);
});
