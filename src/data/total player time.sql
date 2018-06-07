select 
	u.DiscordName
	#,g.Game
    #,DATE(InsertDateTime) as Date
    ,count(d.ID) as TotalMinutes 
from watbot.MinuteData d
inner join watbot.Game g on g.ID = d.Game #and g.Game <> 'No Game'
inner join watbot.User u on d.User = u.ID
where g.Game <> 'NoGame'
group by DiscordName
order by TotalMinutes desc
#Game,
#DATE(InsertDateTime)
;