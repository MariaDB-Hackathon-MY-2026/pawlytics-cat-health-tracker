-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Apr 29, 2026 at 10:50 AM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.1.25

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `kibble_db`
--

DELIMITER $$
--
-- Procedures
--
CREATE DEFINER=`root`@`localhost` PROCEDURE `calculate_kibble_rating` (IN `p_protein` DECIMAL(5,2), IN `p_fat` DECIMAL(5,2), IN `p_fiber` DECIMAL(5,2), OUT `p_rating` CHAR(1))   BEGIN
    DECLARE score INT DEFAULT 0;
    
    -- Protein scoring (35+ = excellent)
    IF p_protein >= 35 THEN
        SET score = score + 40;
    ELSEIF p_protein >= 30 THEN
        SET score = score + 30;
    ELSEIF p_protein >= 25 THEN
        SET score = score + 20;
    ELSE
        SET score = score + 10;
    END IF;
    
    -- Fat scoring (12-18% = ideal for cats)
    IF p_fat BETWEEN 12 AND 18 THEN
        SET score = score + 30;
    ELSEIF p_fat BETWEEN 10 AND 20 THEN
        SET score = score + 20;
    ELSE
        SET score = score + 10;
    END IF;
    
    -- Fiber scoring (3-6% = good)
    IF p_fiber BETWEEN 3 AND 6 THEN
        SET score = score + 30;
    ELSEIF p_fiber BETWEEN 2 AND 8 THEN
        SET score = score + 20;
    ELSE
        SET score = score + 10;
    END IF;
    
    -- Convert score to letter grade
    IF score >= 80 THEN
        SET p_rating = 'A';
    ELSEIF score >= 65 THEN
        SET p_rating = 'B';
    ELSEIF score >= 50 THEN
        SET p_rating = 'C';
    ELSEIF score >= 35 THEN
        SET p_rating = 'D';
    ELSE
        SET p_rating = 'F';
    END IF;
END$$

DELIMITER ;

-- --------------------------------------------------------

--
-- Table structure for table `cats`
--

CREATE TABLE `cats` (
  `id` int(11) NOT NULL,
  `name` varchar(50) NOT NULL,
  `age_months` int(11) NOT NULL CHECK (`age_months` > 0),
  `weight_kg` decimal(5,2) NOT NULL CHECK (`weight_kg` > 0),
  `gender` enum('Male','Female','Unknown') DEFAULT 'Unknown',
  `neutered` tinyint(1) DEFAULT 0,
  `condition_score` enum('Underweight','Ideal','Overweight','Obese') DEFAULT 'Ideal',
  `bcs_numeric` tinyint(4) DEFAULT NULL CHECK (`bcs_numeric` between 1 and 9),
  `activity_level` enum('Sedentary','Moderate','Active','Very Active') DEFAULT 'Moderate',
  `health_conditions` text DEFAULT NULL,
  `daily_calories_need` int(11) GENERATED ALWAYS AS (round(70 * pow(`weight_kg`,0.75) * case `activity_level` when 'Sedentary' then 1.0 when 'Moderate' then 1.2 when 'Active' then 1.4 when 'Very Active' then 1.6 else 1.2 end,0)) VIRTUAL,
  `owner_name` varchar(100) DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `user_id` varchar(50) DEFAULT NULL,
  `user_name` varchar(100) DEFAULT NULL,
  `breed` varchar(100) DEFAULT 'Mixed',
  `age_years` int(11) DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `cats`
--

INSERT INTO `cats` (`id`, `name`, `age_months`, `weight_kg`, `gender`, `neutered`, `condition_score`, `bcs_numeric`, `activity_level`, `health_conditions`, `owner_name`, `created_at`, `updated_at`, `user_id`, `user_name`, `breed`, `age_years`) VALUES
(1, 'Luna', 24, 4.20, 'Female', 1, 'Ideal', 5, 'Moderate', NULL, 'Ahmad', '2026-04-26 05:47:21', '2026-04-26 05:47:21', NULL, NULL, 'Mixed', 0),
(2, 'Simba', 36, 5.80, 'Male', 1, 'Overweight', 7, 'Sedentary', NULL, 'Sarah', '2026-04-26 05:47:21', '2026-04-26 05:47:21', NULL, NULL, 'Mixed', 0),
(3, 'Mimi', 12, 3.50, 'Female', 0, 'Ideal', 5, 'Active', NULL, 'Wei Ling', '2026-04-26 05:47:21', '2026-04-26 05:47:21', NULL, NULL, 'Mixed', 0),
(4, 'Tiger', 48, 6.20, 'Male', 1, 'Obese', 8, 'Sedentary', NULL, 'Kumar', '2026-04-26 05:47:21', '2026-04-26 05:47:21', NULL, NULL, 'Mixed', 0),
(5, 'Whiskers', 18, 3.80, 'Male', 1, 'Underweight', 3, 'Very Active', NULL, 'Fatimah', '2026-04-26 05:47:21', '2026-04-26 05:47:21', NULL, NULL, 'Mixed', 0),
(6, 'Cenonet', 8, 6.00, 'Male', 0, 'Ideal', NULL, 'Active', NULL, NULL, '2026-04-26 15:19:53', '2026-04-26 15:19:53', '61409aa1', 'John', 'Mixed', 0),
(7, 'Yembus', 6, 5.00, 'Female', 0, 'Ideal', NULL, 'Active', NULL, NULL, '2026-04-28 05:45:48', '2026-04-28 05:45:48', '61409aa1', 'John', 'Mixed', 0),
(8, 'Bonga', 7, 6.00, 'Female', 0, 'Ideal', NULL, 'Active', NULL, NULL, '2026-04-29 03:55:45', '2026-04-29 03:55:45', '61409aa1', 'John', 'Mixed', 0),
(9, 'Mambo', 9, 7.20, 'Male', 0, 'Overweight', 7, 'Active', NULL, NULL, '2026-04-29 04:24:42', '2026-04-29 04:24:42', '61409aa1', 'John', 'Mixed', 0);

-- --------------------------------------------------------

--
-- Table structure for table `chat_history`
--

CREATE TABLE `chat_history` (
  `id` int(11) NOT NULL,
  `user_session` varchar(100) NOT NULL,
  `message` text NOT NULL,
  `response` text NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `chat_history`
--

INSERT INTO `chat_history` (`id`, `user_session`, `message`, `response`, `created_at`) VALUES
(1, 'b7b6b61a-b671-4cab-8f8a-db2bf6efd0d5', 'Whiskas vs Royal Canin?', 'As an expert cat nutritionist, let\'s break down Whiskas and Royal Canin based on AAFCO standards and scientific evidence. It\'s not always a simple \"good vs. bad,\" but rather a spectrum of nutritional philosophy, ingredient quality, and scientific rigor.\n\nFirst, a crucial point: **AAFCO (Association of American Feed Control Officials) standards** dictate the minimum and maximum nutrient levels required for a pet food to be labeled \"complete and balanced\" for a specific life stage (e.g., \"adult maintenance,\" \"growth and reproduction\"). Both Whiskas and Royal Canin products *must* meet these standards to be legally sold as complete cat food in regulated markets. However, meeting the *minimum* AAFCO requirements does not mean a food is *optimal* or of the *highest quality*.\n\nNow, let\'s compare:\n\n## Whiskas\n\n**Philosophy:** Whiskas is generally positioned as an affordable, widely available, and palatable option for the general pet owner. Their focus is on meeting basic nutritional needs and appealing to cats\' taste preferences.\n\n**Ingredient Quality and Sourcing:**\n*   **Often uses a blend of animal derivatives and plant-based ingredients.** You\'ll frequently see ingredients like \"meat and animal derivatives\" (which can include various parts like organs, bones, and rendered tissue), cereals (corn, wheat), and vegetable protein extracts. While not inherently \"bad\" (AAFCO allows for these), the *quality and consistency* of these ingredients can be variable compared to premium brands.\n*   **Can contain artificial colors and flavors:** These are often added to enhance visual appeal to owners and palatability, but they offer no nutritional benefit and some cats can be sensitive to them.\n*   **Nutrient Profile:** While meeting AAFCO minimums, the macronutrient profile (protein, fat, carbohydrates) may be less optimized for an obligate carnivore like a cat. They often tend to have higher carbohydrate content from grain fillers.\n*   **Digestibility:** Due to the potential for lower-quality or less digestible ingredients, some cats might have more digestive issues or produce more waste on a Whiskas diet compared to highly digestible premium foods.\n*   **Specialization:** Whiskas offers basic age-specific formulas (kitten, adult, senior) but generally lacks the highly specialized, condition-specific, or breed-specific diets found in premium brands.\n\n**Scientific Evidence & Research:** Whiskas (Mars Petcare) does conduct research, but their primary focus isn\'t on specialized, therapeutic nutrition in the same way Royal Canin is. Their formulations aim for broad acceptance and palatability.\n\n## Royal Canin\n\n**Philosophy:** Royal Canin distinguishes itself through a philosophy of \"precision nutrition.\" They emphasize scientifically formulated diets tailored to specific cat needs based on age, breed, lifestyle, sensitivities, and health conditions. Their approach is heavily research-driven and often veterinary-backed.\n\n**Ingredient Quality and Sourcing:**\n*   **Focus on Nutrient Delivery, not just \"Human-Grade\":** Royal Canin often uses ingredients that might seem less appealing to owners (e.g., chicken by-product meal, corn, rice). However, their rationale is that these ingredients are chosen for their consistent nutrient profile, high digestibility, and specific functional properties to deliver precise nutrition, rather than relying on \"whole\" or \"human-grade\" marketing that might not translate to optimal nutrient delivery for a cat.\n*   **Consistent Quality:** They prioritize consistent sourcing and processing to ensure precise nutrient levels in every batch.\n*   **Nutrient Profile:** Their diets are meticulously formulated for optimal macronutrient ratios (high protein, moderate fat, controlled carbohydrates) and specific micronutrients to support particular health outcomes (e.g., urinary health, coat health, digestive sensitivity).\n*   **Digestibility:** Royal Canin diets are generally highly digestible, leading to better nutrient absorption and often smaller, firmer stools.\n*   **Specialization:** This is where Royal Canin excels. They offer an extensive range of breed-specific diets, life-stage diets, lifestyle-specific diets (e.g., indoor, outdoor), and a significant line of *veterinary therapeutic diets* that require a prescription for specific medical conditions (e.g., kidney disease, diabetes, gastrointestinal issues, allergies).\n\n**Scientific Evidence & Research:** Royal Canin invests heavily in research and development. They collaborate with veterinarians and scientists, publish studies, and use their findings to formulate their diets. This scientific rigor is a cornerstone of their brand.\n\n## Key Differentiators Summarized:\n\n| Feature                   | Whiskas                                   | Royal Canin                                        |\n| :------------------------ | :---------------------------------------- | :------------------------------------------------- |\n| **Nutritional Philosophy** | Basic, palatable, affordable              | Precision nutrition, tailored, research-driven     |\n| **Ingredient Selection**  | Variable quality, broad appeal           | Chosen for consistent nutrient delivery, digestibility |\n| **Nutrient Precision**    | Meets AAFCO minimums, less optimized     | Exceeds AAFCO, highly optimized for specific needs |\n| **Specialization**        | Basic age-based formulas                  | Extensive range: breed, age, lifestyle, therapeutic |\n| **R&D / Scientific Backing** | General R&D                               | Extensive, veterinary collaboration, published research |\n| **Cost**                  | Lower, budget-friendly                    | Higher, premium-priced                             |\n| **Target Audience**       | General cat owners, budget-conscious      | Owners seeking specialized, science-backed nutrition |\n\n## Conclusion: Whiskas vs. Royal Canin\n\nFrom an expert cat nutritionist\'s perspective, **Royal Canin offers a significantly more advanced, scientifically-driven, and tailored nutritional approach compared to Whiskas.**\n\n*   **For a cat with specific health issues, breed predispositions, or unique needs, Royal Canin is almost invariably the superior choice.** Their therapeutic lines are indispensable in veterinary medicine.\n*   **For a healthy, adult cat with no known issues, Whiskas *can* provide basic nutrition that meets AAFCO minimums.** However, it\'s generally considered a less optimal choice due to potentially lower quality/consistency of ingredients, higher carbohydrate content, and lack of refined nutrient profiles compared to premium brands. Long-term, feeding a diet like Royal Canin could contribute to better overall health and disease prevention.\n\n**Recommendation:**\nAlways consult with your veterinarian to determine the best diet for your individual cat, taking into account their age, activity level, health status, and any specific dietary requirements. While Whiskas can be a budget-friendly option, Royal Canin provides a more robust, scientifically-formulated approach to feline nutrition that is often recommended by veterinary professionals for optimal health.', '2026-04-26 05:58:21');

-- --------------------------------------------------------

--
-- Table structure for table `feeding_logs`
--

CREATE TABLE `feeding_logs` (
  `id` int(11) NOT NULL,
  `cat_id` int(11) NOT NULL,
  `kibble_id` int(11) NOT NULL,
  `date_recorded` date NOT NULL,
  `meal_time` enum('Breakfast','Lunch','Dinner','Snack') DEFAULT 'Dinner',
  `amount_grams` decimal(6,2) DEFAULT 0.00,
  `appetite` enum('Poor','Normal','Good','Excellent') DEFAULT 'Normal',
  `notes` text DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `feeding_logs`
--

INSERT INTO `feeding_logs` (`id`, `cat_id`, `kibble_id`, `date_recorded`, `meal_time`, `amount_grams`, `appetite`, `notes`, `created_at`) VALUES
(1, 1, 2, '2026-04-26', 'Breakfast', 45.00, 'Good', NULL, '2026-04-26 05:47:21'),
(2, 1, 2, '2026-04-25', 'Dinner', 50.00, 'Excellent', NULL, '2026-04-26 05:47:21'),
(3, 1, 2, '2026-04-24', 'Breakfast', 45.00, 'Good', NULL, '2026-04-26 05:47:21'),
(4, 2, 1, '2026-04-26', 'Dinner', 60.00, 'Normal', NULL, '2026-04-26 05:47:21'),
(5, 2, 1, '2026-04-25', 'Breakfast', 55.00, 'Good', NULL, '2026-04-26 05:47:21'),
(6, 3, 4, '2026-04-26', 'Breakfast', 40.00, 'Excellent', NULL, '2026-04-26 05:47:21'),
(7, 3, 4, '2026-04-25', 'Dinner', 42.00, 'Good', NULL, '2026-04-26 05:47:21');

-- --------------------------------------------------------

--
-- Table structure for table `health_alerts`
--

CREATE TABLE `health_alerts` (
  `id` int(11) NOT NULL,
  `cat_id` int(11) NOT NULL,
  `alert_type` varchar(50) NOT NULL,
  `message` text NOT NULL,
  `severity` enum('low','medium','high') DEFAULT 'medium',
  `is_read` tinyint(1) DEFAULT 0,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `health_alerts`
--

INSERT INTO `health_alerts` (`id`, `cat_id`, `alert_type`, `message`, `severity`, `is_read`, `created_at`) VALUES
(1, 9, 'overweight', 'Mambo is overweight. Consider adjusting diet and increasing activity.', 'medium', 0, '2026-04-29 04:24:42');

-- --------------------------------------------------------

--
-- Table structure for table `kibbles`
--

CREATE TABLE `kibbles` (
  `id` int(11) NOT NULL,
  `brand_name` varchar(100) NOT NULL,
  `product_line` varchar(100) DEFAULT 'General',
  `protein_pct` decimal(5,2) NOT NULL CHECK (`protein_pct` between 0 and 100),
  `fat_pct` decimal(5,2) NOT NULL CHECK (`fat_pct` between 0 and 100),
  `fiber_pct` decimal(5,2) NOT NULL CHECK (`fiber_pct` between 0 and 100),
  `moisture_pct` decimal(5,2) NOT NULL CHECK (`moisture_pct` between 0 and 100),
  `ash_pct` decimal(5,2) DEFAULT 0.00 CHECK (`ash_pct` between 0 and 100),
  `nfe_pct` decimal(5,2) GENERATED ALWAYS AS (100 - (`protein_pct` + `fat_pct` + `fiber_pct` + `moisture_pct` + `ash_pct`)) VIRTUAL,
  `protein_dmb` decimal(5,2) GENERATED ALWAYS AS (`protein_pct` / (100 - `moisture_pct`) * 100) VIRTUAL,
  `price_per_kg` decimal(10,2) DEFAULT 0.00,
  `package_sizes` varchar(100) DEFAULT '1kg, 2kg, 5kg',
  `rating` char(1) DEFAULT NULL CHECK (`rating` in ('A','B','C','D','F')),
  `ingredients_list` text DEFAULT NULL,
  `has_grain` tinyint(1) DEFAULT 0,
  `has_byproducts` tinyint(1) DEFAULT 0,
  `country_of_origin` varchar(50) DEFAULT 'Malaysia',
  `aafco_approved` tinyint(1) DEFAULT 0,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `user_id` varchar(50) DEFAULT NULL,
  `user_name` varchar(100) DEFAULT NULL,
  `product_name` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `kibbles`
--

INSERT INTO `kibbles` (`id`, `brand_name`, `product_line`, `protein_pct`, `fat_pct`, `fiber_pct`, `moisture_pct`, `ash_pct`, `price_per_kg`, `package_sizes`, `rating`, `ingredients_list`, `has_grain`, `has_byproducts`, `country_of_origin`, `aafco_approved`, `created_at`, `updated_at`, `user_id`, `user_name`, `product_name`) VALUES
(1, 'Whiskas Adult Chicken', 'Adult Maintenance', 30.00, 10.00, 5.00, 12.00, 8.00, 18.50, '1kg, 2kg, 5kg', 'B', NULL, 1, 0, 'Malaysia', 1, '2026-04-26 05:47:21', '2026-04-26 05:47:21', NULL, NULL, NULL),
(2, 'Royal Canin Indoor 27', 'Indoor Adult', 35.00, 14.00, 6.00, 8.00, 7.50, 65.00, '1kg, 2kg, 5kg', 'A', NULL, 0, 0, 'Malaysia', 1, '2026-04-26 05:47:21', '2026-04-26 05:47:21', NULL, NULL, NULL),
(3, 'Smart Heart Adult', 'Budget Line', 28.00, 9.00, 4.50, 12.00, 9.00, 12.00, '1kg, 2kg, 5kg', 'C', NULL, 1, 0, 'Malaysia', 0, '2026-04-26 05:47:21', '2026-04-26 05:47:21', NULL, NULL, NULL),
(4, 'Pro Plan Adult Chicken', 'Premium', 38.00, 16.00, 2.50, 10.00, 7.00, 72.00, '1kg, 2kg, 5kg', 'A', NULL, 0, 0, 'Malaysia', 1, '2026-04-26 05:47:21', '2026-04-26 05:47:21', NULL, NULL, NULL),
(5, 'MeowMix Original', 'Value', 26.00, 8.50, 5.50, 12.00, 8.50, 15.00, '1kg, 2kg, 5kg', 'C', NULL, 1, 0, 'Malaysia', 1, '2026-04-26 05:47:21', '2026-04-26 05:47:21', NULL, NULL, NULL),
(6, 'Friskies Seafood', 'Budget', 27.00, 9.00, 4.00, 12.00, 8.00, 14.50, '1kg, 2kg, 5kg', 'C', NULL, 1, 0, 'Malaysia', 1, '2026-04-26 05:47:21', '2026-04-26 05:47:21', NULL, NULL, NULL),
(7, 'Hill\'s Science Diet Adult', 'Veterinary', 34.00, 15.50, 3.00, 9.00, 6.50, 85.00, '1kg, 2kg, 5kg', 'A', NULL, 0, 0, 'Malaysia', 1, '2026-04-26 05:47:21', '2026-04-26 05:47:21', NULL, NULL, NULL),
(8, 'Orijen Cat & Kitten', 'Biologically Appropriate', 42.00, 20.00, 3.00, 10.00, 8.00, 120.00, '1kg, 2kg, 5kg', 'A', NULL, 0, 0, 'Malaysia', 1, '2026-04-26 05:47:21', '2026-04-26 05:47:21', NULL, NULL, NULL),
(9, 'Catz Finefood', 'Mid-Range', 32.00, 13.00, 4.00, 10.00, 7.00, 45.00, '1kg, 2kg, 5kg', 'B', NULL, 0, 0, 'Malaysia', 1, '2026-04-26 05:47:21', '2026-04-26 05:47:21', NULL, NULL, NULL),
(10, 'FancyFeast Classic', 'Gourmet', 30.00, 11.00, 4.50, 11.00, 7.50, 35.00, '1kg, 2kg, 5kg', 'B', NULL, 0, 0, 'Malaysia', 1, '2026-04-26 05:47:21', '2026-04-26 05:47:21', NULL, NULL, NULL),
(12, 'ROYAL CANIN', 'General', 11.80, 2.20, 0.80, 77.70, 2.20, 40.00, '1kg, 2kg, 5kg', 'A', NULL, 0, 0, 'Malaysia', 0, '2026-04-26 15:23:44', '2026-04-26 15:23:44', '61409aa1', 'John', 'ROYAL CANIN'),
(13, 'Purina', 'General', 28.00, 9.00, 5.00, 12.00, 0.00, 20.00, '1kg, 2kg, 5kg', 'C', NULL, 0, 0, 'Malaysia', 0, '2026-04-29 04:36:08', '2026-04-29 04:36:08', '61409aa1', 'John', 'Purina');

-- --------------------------------------------------------

--
-- Table structure for table `nutrition_standards`
--

CREATE TABLE `nutrition_standards` (
  `id` int(11) NOT NULL,
  `life_stage` enum('Kitten','Adult','Senior','Pregnant') NOT NULL,
  `nutrient_name` varchar(50) NOT NULL,
  `min_percentage` decimal(5,2) DEFAULT NULL,
  `max_percentage` decimal(5,2) DEFAULT NULL,
  `unit` varchar(20) DEFAULT '%',
  `source` varchar(100) DEFAULT 'AAFCO 2023',
  `notes` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `nutrition_standards`
--

INSERT INTO `nutrition_standards` (`id`, `life_stage`, `nutrient_name`, `min_percentage`, `max_percentage`, `unit`, `source`, `notes`) VALUES
(1, 'Adult', 'Crude Protein', 26.00, NULL, '%', 'AAFCO 2023', NULL),
(2, 'Adult', 'Crude Fat', 9.00, NULL, '%', 'AAFCO 2023', NULL),
(3, 'Adult', 'Crude Fiber', NULL, 8.00, '%', 'AAFCO 2023', NULL),
(4, 'Kitten', 'Crude Protein', 30.00, NULL, '%', 'AAFCO 2023', NULL),
(5, 'Kitten', 'Crude Fat', 12.00, NULL, '%', 'AAFCO 2023', NULL),
(6, 'Senior', 'Crude Protein', 28.00, NULL, '%', 'AAFCO 2023', NULL),
(7, 'Senior', 'Crude Fiber', NULL, 6.00, '%', 'AAFCO 2023', NULL);

-- --------------------------------------------------------

--
-- Table structure for table `scan_history`
--

CREATE TABLE `scan_history` (
  `id` int(11) NOT NULL,
  `session_id` varchar(100) DEFAULT NULL,
  `kibble_id` int(11) DEFAULT NULL,
  `scan_type` enum('label','cat_photo','custom') DEFAULT 'label',
  `result_data` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL CHECK (json_valid(`result_data`)),
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `user_id` varchar(50) DEFAULT NULL,
  `user_name` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `scan_history`
--

INSERT INTO `scan_history` (`id`, `session_id`, `kibble_id`, `scan_type`, `result_data`, `created_at`, `user_id`, `user_name`) VALUES
(2, 'f514c5cd-0429-477b-83a9-78979a590b96', 12, 'label', '{\"brand_name\": \"ROYAL CANIN\", \"product_line\": \"HAIR&SKIN\", \"protein_pct\": 11.8, \"fat_pct\": 2.2, \"fiber_pct\": 0.8, \"moisture_pct\": 77.7, \"ash_pct\": 2.2, \"price_per_kg\": 0.0}', '2026-04-26 15:23:44', NULL, NULL),
(3, 'fb77a435-4730-47e7-b602-a7929f1310bf', 13, 'label', '{\"brand_name\": \"Purina\", \"product_line\": \"Friskies\", \"protein_pct\": 28.0, \"fat_pct\": 9.0, \"fiber_pct\": 5.0, \"moisture_pct\": 12.0, \"ash_pct\": 0.0, \"price_per_kg\": 0.0}', '2026-04-29 04:36:08', NULL, NULL);

-- --------------------------------------------------------

--
-- Stand-in structure for view `v_cat_health`
-- (See below for the actual view)
--
CREATE TABLE `v_cat_health` (
`id` int(11)
,`name` varchar(50)
,`age_months` int(11)
,`weight_kg` decimal(5,2)
,`condition_score` enum('Underweight','Ideal','Overweight','Obese')
,`activity_level` enum('Sedentary','Moderate','Active','Very Active')
,`daily_calories_need` int(11)
,`brands_tried` bigint(21)
,`total_meals_logged` bigint(21)
,`last_feeding_date` date
,`days_since_last_log` int(7)
);

-- --------------------------------------------------------

--
-- Stand-in structure for view `v_dashboard_stats`
-- (See below for the actual view)
--
CREATE TABLE `v_dashboard_stats` (
`total_cats` bigint(21)
,`total_kibbles` bigint(21)
,`total_brands` bigint(21)
,`total_feedings` bigint(21)
,`avg_protein` decimal(9,6)
,`avg_quality_score` decimal(6,5)
);

-- --------------------------------------------------------

--
-- Stand-in structure for view `v_feeding_trends`
-- (See below for the actual view)
--
CREATE TABLE `v_feeding_trends` (
`feeding_date` date
,`cat_name` varchar(50)
,`brand_name` varchar(100)
,`total_grams` decimal(28,2)
,`meal_count` bigint(21)
,`avg_appetite` decimal(4,4)
);

-- --------------------------------------------------------

--
-- Stand-in structure for view `v_kibble_analytics`
-- (See below for the actual view)
--
CREATE TABLE `v_kibble_analytics` (
`id` int(11)
,`brand_name` varchar(100)
,`product_line` varchar(100)
,`protein_pct` decimal(5,2)
,`fat_pct` decimal(5,2)
,`nfe_pct` decimal(5,2)
,`protein_dmb` decimal(5,2)
,`price_per_kg` decimal(10,2)
,`rating` char(1)
,`cats_fed` bigint(21)
,`total_feedings` bigint(21)
,`protein_value_ratio` decimal(8,2)
,`avg_appetite_score` decimal(3,2)
);

-- --------------------------------------------------------

--
-- Structure for view `v_cat_health`
--
DROP TABLE IF EXISTS `v_cat_health`;

CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `v_cat_health`  AS SELECT `c`.`id` AS `id`, `c`.`name` AS `name`, `c`.`age_months` AS `age_months`, `c`.`weight_kg` AS `weight_kg`, `c`.`condition_score` AS `condition_score`, `c`.`activity_level` AS `activity_level`, `c`.`daily_calories_need` AS `daily_calories_need`, count(distinct `fl`.`kibble_id`) AS `brands_tried`, count(`fl`.`id`) AS `total_meals_logged`, max(`fl`.`date_recorded`) AS `last_feeding_date`, to_days(curdate()) - to_days(max(`fl`.`date_recorded`)) AS `days_since_last_log` FROM (`cats` `c` left join `feeding_logs` `fl` on(`c`.`id` = `fl`.`cat_id`)) GROUP BY `c`.`id` ;

-- --------------------------------------------------------

--
-- Structure for view `v_dashboard_stats`
--
DROP TABLE IF EXISTS `v_dashboard_stats`;

CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `v_dashboard_stats`  AS SELECT (select count(0) from `cats`) AS `total_cats`, (select count(0) from `kibbles`) AS `total_kibbles`, (select count(distinct `kibbles`.`brand_name`) from `kibbles`) AS `total_brands`, (select count(0) from `feeding_logs`) AS `total_feedings`, (select avg(`kibbles`.`protein_pct`) from `kibbles`) AS `avg_protein`, (select avg(case `kibbles`.`rating` when 'A' then 5.0 when 'B' then 4.0 when 'C' then 3.0 when 'D' then 2.0 else 1.0 end) from `kibbles`) AS `avg_quality_score` ;

-- --------------------------------------------------------

--
-- Structure for view `v_feeding_trends`
--
DROP TABLE IF EXISTS `v_feeding_trends`;

CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `v_feeding_trends`  AS SELECT cast(`fl`.`date_recorded` as date) AS `feeding_date`, `c`.`name` AS `cat_name`, `k`.`brand_name` AS `brand_name`, sum(`fl`.`amount_grams`) AS `total_grams`, count(0) AS `meal_count`, avg(case `fl`.`appetite` when 'Poor' then 1 when 'Normal' then 2 when 'Good' then 3 when 'Excellent' then 4 end) AS `avg_appetite` FROM ((`feeding_logs` `fl` join `cats` `c` on(`fl`.`cat_id` = `c`.`id`)) join `kibbles` `k` on(`fl`.`kibble_id` = `k`.`id`)) WHERE `fl`.`date_recorded` >= curdate() - interval 30 day GROUP BY cast(`fl`.`date_recorded` as date), `fl`.`cat_id`, `fl`.`kibble_id` ORDER BY cast(`fl`.`date_recorded` as date) DESC ;

-- --------------------------------------------------------

--
-- Structure for view `v_kibble_analytics`
--
DROP TABLE IF EXISTS `v_kibble_analytics`;

CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `v_kibble_analytics`  AS SELECT `k`.`id` AS `id`, `k`.`brand_name` AS `brand_name`, `k`.`product_line` AS `product_line`, `k`.`protein_pct` AS `protein_pct`, `k`.`fat_pct` AS `fat_pct`, `k`.`nfe_pct` AS `nfe_pct`, `k`.`protein_dmb` AS `protein_dmb`, `k`.`price_per_kg` AS `price_per_kg`, `k`.`rating` AS `rating`, count(distinct `fl`.`cat_id`) AS `cats_fed`, count(`fl`.`id`) AS `total_feedings`, round(`k`.`protein_pct` / nullif(`k`.`price_per_kg`,0),2) AS `protein_value_ratio`, round(avg(case `fl`.`appetite` when 'Poor' then 1 when 'Normal' then 2 when 'Good' then 3 when 'Excellent' then 4 end),2) AS `avg_appetite_score` FROM (`kibbles` `k` left join `feeding_logs` `fl` on(`k`.`id` = `fl`.`kibble_id`)) GROUP BY `k`.`id` ORDER BY round(`k`.`protein_pct` / nullif(`k`.`price_per_kg`,0),2) DESC ;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `cats`
--
ALTER TABLE `cats`
  ADD PRIMARY KEY (`id`),
  ADD KEY `idx_condition` (`condition_score`),
  ADD KEY `idx_activity` (`activity_level`),
  ADD KEY `idx_user_id` (`user_id`);

--
-- Indexes for table `chat_history`
--
ALTER TABLE `chat_history`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `feeding_logs`
--
ALTER TABLE `feeding_logs`
  ADD PRIMARY KEY (`id`),
  ADD KEY `idx_cat_date` (`cat_id`,`date_recorded`),
  ADD KEY `idx_kibble_date` (`kibble_id`,`date_recorded`);

--
-- Indexes for table `health_alerts`
--
ALTER TABLE `health_alerts`
  ADD PRIMARY KEY (`id`),
  ADD KEY `cat_id` (`cat_id`);

--
-- Indexes for table `kibbles`
--
ALTER TABLE `kibbles`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `brand_name` (`brand_name`),
  ADD KEY `idx_rating` (`rating`),
  ADD KEY `idx_price` (`price_per_kg`),
  ADD KEY `idx_protein` (`protein_pct`),
  ADD KEY `idx_user_id` (`user_id`);
ALTER TABLE `kibbles` ADD FULLTEXT KEY `idx_brand` (`brand_name`,`product_line`);

--
-- Indexes for table `nutrition_standards`
--
ALTER TABLE `nutrition_standards`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `unique_standard` (`life_stage`,`nutrient_name`);

--
-- Indexes for table `scan_history`
--
ALTER TABLE `scan_history`
  ADD PRIMARY KEY (`id`),
  ADD KEY `kibble_id` (`kibble_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `cats`
--
ALTER TABLE `cats`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;

--
-- AUTO_INCREMENT for table `chat_history`
--
ALTER TABLE `chat_history`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `feeding_logs`
--
ALTER TABLE `feeding_logs`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT for table `health_alerts`
--
ALTER TABLE `health_alerts`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `kibbles`
--
ALTER TABLE `kibbles`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=14;

--
-- AUTO_INCREMENT for table `nutrition_standards`
--
ALTER TABLE `nutrition_standards`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT for table `scan_history`
--
ALTER TABLE `scan_history`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `feeding_logs`
--
ALTER TABLE `feeding_logs`
  ADD CONSTRAINT `feeding_logs_ibfk_1` FOREIGN KEY (`cat_id`) REFERENCES `cats` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `feeding_logs_ibfk_2` FOREIGN KEY (`kibble_id`) REFERENCES `kibbles` (`id`);

--
-- Constraints for table `health_alerts`
--
ALTER TABLE `health_alerts`
  ADD CONSTRAINT `health_alerts_ibfk_1` FOREIGN KEY (`cat_id`) REFERENCES `cats` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `scan_history`
--
ALTER TABLE `scan_history`
  ADD CONSTRAINT `scan_history_ibfk_1` FOREIGN KEY (`kibble_id`) REFERENCES `kibbles` (`id`) ON DELETE SET NULL;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
