select 
	u.DiscordName
	,g.Game
    ,count(d.ID) 
from watbot.MinuteData d
inner join watbot.Game g on g.ID = d.Game
inner join watbot.User u on d.User = u.ID
group by DiscordName,Game
;