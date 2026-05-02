-- ============================================================
-- VitaClin — Queries Analíticas
-- Base: tabela atendimentos (PostgreSQL)
-- Observação: as queries de cidade (TOP cidades e Faturamento RJ)
-- dependem da tabela `clientes`, disponível apenas no banco
-- PostgreSQL — não presente no arquivo CSV exportado.
-- ============================================================


-- Faturamento por grupo de procedimento
SELECT 
    grupoprocedimento,
    SUM(valor_pago) AS faturamento
FROM atendimentos
GROUP BY grupoprocedimento
ORDER BY faturamento DESC;


-- Quantidade de atendimentos por grupo de procedimento
SELECT 
    grupoprocedimento,
    COUNT(*) AS quantidade
FROM atendimentos
GROUP BY grupoprocedimento
ORDER BY quantidade DESC;


-- TOP pacientes (valor + quantidade)
SELECT 
    paciente_id,
    COUNT(*) AS total_atendimentos,
    SUM(valor_pago) AS valor_total
FROM atendimentos
WHERE grupoprocedimento IN ('Psiquiatria', 'Clínica Geral', 'Endocrinologia')
GROUP BY paciente_id
ORDER BY valor_total DESC
LIMIT 10;


-- TOP cidades (receita + quantidade)
-- Requer JOIN com a tabela `clientes` (banco PostgreSQL)
SELECT 
    c.cidade,
    COUNT(*) AS quantidade_atendimentos,
    SUM(a.valor_pago) AS receita_total
FROM atendimentos a
JOIN clientes c 
    ON a.paciente_id = c.paciente_id
GROUP BY c.cidade
ORDER BY receita_total DESC;


-- Faturamento total — pacientes do RJ
-- Requer JOIN com a tabela `clientes` (banco PostgreSQL)
SELECT 
    SUM(a.valor_pago) AS faturamento_rj
FROM atendimentos a
JOIN clientes c 
    ON a.paciente_id = c.paciente_id
WHERE LOWER(c.cidade) = 'rio de janeiro';


-- Pacientes que retornaram no mês seguinte
SELECT DISTINCT a1.paciente_id
FROM atendimentos a1
JOIN atendimentos a2
    ON a1.paciente_id = a2.paciente_id
WHERE DATE_TRUNC('month', a2.data_atendimento) = 
      DATE_TRUNC('month', a1.data_atendimento + INTERVAL '1 month');
