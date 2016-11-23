CREATE TABLE IF NOT EXISTS `results` (
  `id` int(11) NOT NULL,
  `stage_id` int(11) NOT NULL,
  `player_id` int(11) NOT NULL,
  `driver` varchar(250) NOT NULL,
  `car` varchar(250) NOT NULL,
  `time` int(11) NOT NULL,
  `nationality` int(11) NOT NULL,
  `founder` tinyint(1) NOT NULL,
  `vip` tinyint(1) NOT NULL,
  `platform` varchar(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


CREATE TABLE IF NOT EXISTS `stages` (
  `id` int(11) NOT NULL,
  `location_id` smallint(6) NOT NULL,
  `weather_icon` varchar(30) NOT NULL,
  `country` varchar(100) NOT NULL,
  `flag` smallint(6) NOT NULL,
  `stage` varchar(100) NOT NULL,
  `daytime` varchar(100) NOT NULL,
  `weather` varchar(100) NOT NULL,
  `date` date NOT NULL,
  `type` varchar(10) NOT NULL,
  `stageidx` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

ALTER TABLE `results`
  ADD PRIMARY KEY (`id`);

ALTER TABLE `stages`
  ADD PRIMARY KEY (`id`);

ALTER TABLE `results`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

ALTER TABLE `stages`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
