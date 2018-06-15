CREATE DATABASE cc;
USE cc;

CREATE TABLE `nodestatus` (
  `node` varchar(20) NOT NULL,
  `status` int(1) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
ALTER TABLE `nodestatus`
  ADD PRIMARY KEY (`node`);

CREATE TABLE `heartbeat` (
  `node` varchar(20) NOT NULL,
  `time` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
ALTER TABLE `heartbeat`
  ADD PRIMARY KEY (`node`);


CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `username` varchar(20) NOT NULL,
  `password` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`),ADD UNIQUE KEY `username` (`username`);
ALTER TABLE `users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

INSERT INTO `users` (`id`, `username`, `password`) VALUES
(1, 'user1', 'root'),
(2, 'user2', 'root'),
(3, 'user3', 'root'),
(4, 'user4', 'root');

CREATE TABLE `files` (
  `fid` int(11) NOT NULL,
  `uid` int(11) NOT NULL,
  `filename` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

ALTER TABLE `files`
  ADD PRIMARY KEY (`fid`),
  ADD KEY `uid` (`uid`);
ALTER TABLE `files`
  ADD CONSTRAINT `uid` FOREIGN KEY (`uid`) REFERENCES `users` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;

CREATE TABLE `shard` (
  `fid` int(11) NOT NULL,
  `shard_id` varchar(2048) NOT NULL,
  `storage_id` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
ALTER TABLE `shard`
  ADD KEY `fid` (`fid`),
  ADD KEY `storage_id` (`storage_id`);
ALTER TABLE `shard`
  ADD CONSTRAINT `shard_ibfk_1` FOREIGN KEY (`fid`) REFERENCES `files` (`fid`),
  ADD CONSTRAINT `shard_ibfk_2` FOREIGN KEY (`storage_id`) REFERENCES `nodestatus` (`node`);


